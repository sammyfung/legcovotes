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
    mover_type = Field()
    separate_mechanism = Field()
    fc_present = Field()
    fc_vote = Field()
    fc_yes = Field()
    fc_no = Field()
    fc_abstain = Field()
    fc_result = Field()
    gc_present = Field()
    gc_vote = Field()
    gc_yes = Field()
    gc_no = Field()
    gc_abstain = Field()
    gc_result = Field()
    present = Field()
    vote = Field()
    yes = Field()
    no = Field()
    abstain = Field()
    result = Field()


class IndividualVoteItem(Item):
    number = Field()
    date = Field()
    name_ch = Field()
    name_en = Field()
    constituency = Field()
    vote = Field()
