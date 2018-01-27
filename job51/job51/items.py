# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item


class Job51Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = Field()
    url = Field()
    company = Field()
    region = Field()
    salary = Field()
    data = Field()
