legcovotes
==========

This project consists of a web scraper and a Django app, which can be used separately. 

The web scraper collects voting result data of Hong Kong Legislative Council (LegCo) meetings. Data structure defined in items.py is based on the initial version of HKU JMSC [LegcoCouncilVotes](https://github.com/JMSCHKU/LegcoCouncilVotes).


Quickstart of Web Scrapy 
------------------------

```
$ git clone https://github.com/sammyfung/legcovotes.git
$ cd legcovotes
$ python3 -m venv venv   
$ source venv/bin/activate  
$ pip install -r requirements_legcovotesscraper.txt  
$ cd legcovotes  
$ scrapy crawl legcovotes -o testresult.json
```

