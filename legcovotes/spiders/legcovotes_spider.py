from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from legcovotes.items import VoteItem, IndividualVoteItem

import re
from scrapy.http import Request

class LegcovotesSpider(CrawlSpider):
    name = 'legcovotes'
    allowed_domains = ['legco.gov.hk']
    start_urls = ['http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm']

    rules = (
        Rule(SgmlLinkExtractor(allow='mtg_[0-9]*\.htm'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        xmllist = hxs.select('//td/a[contains(@name,"cm")]/@name').extract()
        items = []
        for i in xmllist:
            xmlurl = 'http://www.legco.gov.hk/yr12-13/chinese/counmtg/voting/' + re.sub('cm','cm_vote_',i) + '.xml'
            print "*** %s"%xmlurl
            yield Request(xmlurl, callback=self.parse_xml_document)
            #items = items.append(Request(xmlurl, callback=self.parse_xml_document))
        #return items
   
    def parse_xml_document(self, response):
        xxs = XmlXPathSelector(response)
        votes = xxs.select('//meeting/vote')
        items = []

        for vote in votes:
            councilvote = VoteItem()
            councilvote["number"] = vote.select('@number').extract()
            councilvote["date"] = vote.select('vote-date/text()').extract()
            councilvote["time"] = vote.select('vote-time/text()').extract()
            councilvote["motion_ch"] = vote.select('motion-ch/text()').extract()
            councilvote["motion_en"] = vote.select('motion-en/text()').extract()
            councilvote["mover_ch"] = vote.select('mover-ch/text()').extract()
            councilvote["mover_en"] = vote.select('mover-en/text()').extract()
            councilvote["type"] = vote.select('mover-type/text()').extract()
            councilvote["separate_mechanism"] = vote.select('vote-separate-mechanism/text()').extract()

            items.append(councilvote)

            votenum = int(vote.select('@number').extract()[0])
            members = xxs.select('//meeting/vote[%s]/individual-votes/member'%votenum)
            for member in members:
                individualvote = IndividualVoteItem()
                individualvote['number'] = councilvote["number"]
                individualvote['date'] = councilvote["date"]
                individualvote['name_ch'] = member.select('@name-ch').extract()
                individualvote['name_en'] = member.select('@name-en').extract()
                individualvote['constituency'] = member.select('@constituency').extract()
                individualvote['vote'] = member.select('vote/text()').extract()

                items.append(individualvote)


        return items
