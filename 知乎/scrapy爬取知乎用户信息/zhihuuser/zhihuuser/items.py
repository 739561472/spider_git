# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item


class ZhihuuserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(Item):
    name = Field()
    answer_count = Field()
    articles_count = Field()
    follower_count = Field()
    headline = Field()
    url_token = Field()

