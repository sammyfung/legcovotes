import scrapy
from legcovotes.items import VoteItem, IndividualVoteItem
import re

class LegcovotesSpider(scrapy.Spider):
    name = 'legcovotes'
    allowed_domains = ['legco.gov.hk']
    start_urls = ['http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1213.htm']

    rules = (
        scrapy.spiders.Rule(link_extractor=scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow='mtg_[0-9]*\.htm'), callback='parse', follow=False),
    )

    def parse(self, response):
        xmllist = response.xpath('//td/a[contains(@name,"cm")]/@name').extract()
        items = []
        for i in xmllist:
            xmlurl = 'http://www.legco.gov.hk/yr12-13/chinese/counmtg/voting/' + re.sub('cm','cm_vote_',i) + '.xml'
            yield scrapy.http.Request(url=xmlurl, callback=self.parse_xml_document)
   
    def parse_xml_document(self, response):
        votes = response.xpath('//meeting/vote')
        items = []

        for vote in votes:
            councilvote = VoteItem()
            votenum = int(vote.xpath('@number').extract()[0])
            councilvote["number"] = int(votenum)
            councilvote["date"] = vote.xpath('vote-date/text()').extract()[0]
            councilvote["time"] = vote.xpath('vote-time/text()').extract()[0]
            councilvote["motion_ch"] = vote.xpath('motion-ch/text()').extract()[0]
            councilvote["motion_en"] = vote.xpath('motion-en/text()').extract()[0]
            councilvote["mover_ch"] = vote.xpath('mover-ch/text()').extract()[0]
            councilvote["mover_en"] = vote.xpath('mover-en/text()').extract()[0]
            councilvote["mover_type"] = vote.xpath('mover-type/text()').extract()[0]
            councilvote["separate_mechanism"] = vote.xpath('vote-separate-mechanism/text()').extract()[0]
            if councilvote["separate_mechanism"] == 'Yes':
                mechanism = ['functional-constituency', 'geographical-constituency']
            else:
                mechanism = ['overall']
            for constituency in mechanism:
                if constituency == 'functional-constituency':
                    short = 'fc_'
                elif constituency == 'geographical-constituency':
                    short = 'gc_'
                else:
                    short = ''
                for count_type in ['present', 'vote', 'yes', 'no', 'abstain']:
                    councilvote[short+count_type] = int(vote.xpath('vote-summary/'+constituency+'/'+count_type+'-count/text()').extract()[0])
                councilvote[short+'result'] = vote.xpath('vote-summary/'+constituency+'/'+'result/text()').extract()[0]
            councilvote['result'] = vote.xpath('vote-summary/overall/result/text()').extract()[0]


            items.append(councilvote)

            members = response.xpath('//meeting/vote[%s]/individual-votes/member'%votenum)
            for member in members:
                individualvote = IndividualVoteItem()
                individualvote['number'] = councilvote["number"]
                individualvote['date'] = councilvote["date"]
                individualvote['name_ch'] = member.xpath('@name-ch').extract()[0]
                individualvote['name_en'] = member.xpath('@name-en').extract()[0]
                individualvote['constituency'] = member.xpath('@constituency').extract()[0]
                individualvote['vote'] = member.xpath('vote/text()').extract()[0]

                items.append(individualvote)


        return items
