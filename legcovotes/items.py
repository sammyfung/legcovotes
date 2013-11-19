# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class VoteItem(Item):
    number = Field()
    date = Field()
    time = Field()
    motion_ch = Field()
    motion_en = Field()
    mover_ch = Field()
    mover_en = Field()
    type = Field()
    separate_mechanism = Field()


class IndividualVoteItem(Item):
    number = Field()
    date = Field()
    name_ch = Field()
    name_en = Field()
    constituency = Field()
    vote = Field()
