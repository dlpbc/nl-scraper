import os
import sys
import getopt
import lxml.html
import tqdm
from datetime import datetime
from urllib.request import Request
from urllib.request import urlopen

# Helper function to print srcipt usage command
def print_usage():
    print('Usage:')
    print('\t1. python %s' % __file__)
    print('\t2. python %s -s <start-page-number> -e <end-page-number> [-o <output-file>]' % __file__)
    print('\t3. python %s -h  (for help)\n' % __file__)

# Helper function to parse command line arguments
def parse_args(argv):
    start = end = output_file = None

    try:
        [opts, args] = getopt.getopt(argv, 'hs:e:o:')
    except getopt.GetoptError:
        print_usage()

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt == '-s':
            start = arg
        elif opt == '-e':
            end = arg
        elif opt == '-o':
            output_file = arg


    if start and end:
        try:
            start = int(start)
            end = int(end)
        except ValueError:
            print('ERROR:')
            print('\'start-page-number\' and \'end-page-number\' must be integers.')
            print_usage()
            sys.exit()
    else:
        # set default start and end configuration when argument was not specified by user
        start = 0
        end = 5
        print('\nRange of featured links pages to scrape not completely specified')
        print('Missing argument(s) \'start-page-number\', \'end-page-number\' or both.')
        print('Using default configuration...')
        print('start page number: %d' % start)
        print('end page number: %d' % end)

    print()
    if not output_file:
        output_file = 'nl-scraper-{0}.txt'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('Using default output file: %s\n' % output_file)

    return [start, end, output_file]

def main(start, end, output_file):
    base_url = 'http://www.nairaland.com/links/'
    featured_links_list = []

    print('Fetching and processing featured links page(s) from page %d to %d...' % (start, end))
    for page_num in tqdm.tqdm(range(start, end+1)):
        # fetch page
        url = '{0}{1}'.format(base_url, page_num)
        # set request user-agent as mozilla (any other web browser should as be fine)
        # nairaland does not accept the default python user-agent (responds with forbidden 403)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        str_response = urlopen(req).read()
        str_response = str_response.decode()

        # create html tree structure from html response string
        root = lxml.html.fromstring(str_response)

        # locate the table tag containing the featured links
        # (this is based on the structure of nairaland page)
        featured_links_table_tag = None
        for table in root.iter('table'):
             if table.attrib.get('summary') == 'links':
                 featured_links_table_tag = table
        
        if featured_links_table_tag == None:
            print('There was an issue scrapping %s' % url)
            print('Could not locate the section containing featured links...')

        for a_tag in featured_links_table_tag.iter('a'):
            content = a_tag.text_content()
            content = '{0}\n'.format(content)
            featured_links_list.append(content)

    print('Saving featured links to file %s' % output_file)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(featured_links_list)
    print('Done...')



if __name__ == '__main__':
    start, end, output_file = parse_args(sys.argv[1:])
    main(start, end, output_file)
