legcovotes
==========

Developer: Sammy Fung <sammy@sammy.hk>  
Web Site: http://sammy.hk

It collects result data of Hong Kong Legislative Council (LegCo) Votes from XML files on LegCo website.

It is written in python with scrapy web crawling framework. It is based on data structure (defined in items.py) of inital version of HKU JMSC codes.

Original HKU JMSC codes: https://github.com/JMSCHKU/LegcoCouncilVotes

Installation Example
--------------------

$ virtualenv legcovotesenv  
$ source legcovotesenv/bin/activate  
$ pip install scrapy  
$ git clone https://github.com/sammyfung/legcovotes.git  
$ cd legcovotes/legcovotes  
$ scrapy crawl legcovotes -t json -o testresult  


