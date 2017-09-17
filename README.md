# nl-scraper
Web scraper for **Nairaland** featured links (http://www.nairaland.com/links). Scrape multiple pages of featured links in Nairaland.

## Dependencies (External python package)
1. lxml - xml processing library (parser)
2. html_wrapper - html parser with lxml backend (to parse fetched html pages containing featured links)
3. tqdm - progress bar

## Usage
```
python scraper.py   (default configuration)

OR

python scraper.py -s <start-page-number> -e <end-page-number> [-o <output-file>]

OR

python scraper.py -h (for help)
```

## Default configuration
* start-page-number: 0
* end-page-number: 5
* output-file: nl-scrapper-<current-time-stamp>.txt

## Note
Implemented and tested in **Python 3**
