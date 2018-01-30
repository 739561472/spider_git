# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossjobItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()
    job_id = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    # job_detials = scrapy.Field()
    company = scrapy.Field()
    company_detials = scrapy.Field()
    time = scrapy.Field()
    region = scrapy.Field()
    experice = scrapy.Field()
    grades = scrapy.Field()



