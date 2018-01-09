# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class BooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    price = Field()
    # 将作者名字进行串行化
    authors = Field(serializer = lambda x:'|'.join(x))

class ForeignBooksItem(BooksItem):
    name = Field()
    price = Field()
    traslator = Field()