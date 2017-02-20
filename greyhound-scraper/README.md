##About
**greyhound.ca** doesn't have a way of viewing a table of prices for a date range, like an entire week. This script scrapes the website and puts together a bus fare table for a specified date range.

```
usage: greyhound.py [-h] --origin ORIGIN --destination DESTINATION
                    [--from-date FROM_DATE] [--to-date TO_DATE]

optional arguments:
  -h, --help            show this help message and exit
  --origin ORIGIN, -o ORIGIN
                        the origin, as it appears in the dropdown on the
                        website
  --destination DESTINATION, -d DESTINATION
                        the destination, as it appears in the dropdown on the
                        website
  --from-date FROM_DATE, -f FROM_DATE
                        the starting date (d/m/Y)
  --to-date TO_DATE, -t TO_DATE
                        the ending date (d/m/Y)
```


##Requires
- python2 or python3
- [lxml module](http://lxml.de/)
- [selenium module](http://selenium-python.readthedocs.io/installation.html)
- [Chrome webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) (easiest to just extract to `/usr/bin/local`)

##Useful Resources
- Selenium for Python docs [link](http://selenium-python.readthedocs.io/getting-started.html)
- Hitchhiker's Guide to Python: [Web Scraping](http://docs.python-guide.org/en/latest/scenarios/scrape/)
- Automate The Boring Stuff with Python : [Web Scraping](https://automatetheboringstuff.com/chapter11/)


##Writing output to a google sheet
You'll need to generate a credentials for yourself as described [here](https://developers.google.com/sheets/api/quickstart/python), and then:
```
python greyhound.py --destination "Toronto, ON" --origin "London, ON" --to-date "21/02/2017" | python google_sync.py --sheet-id <sheet-id>
```
