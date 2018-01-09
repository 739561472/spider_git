# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    def start_requests(self):
        yield scrapy.Request(
            'http://www.51job.com/?from=baidupz',
            callback=self.parse(),
            headers={'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'},
            dont_filter=True
        )
    def parse_job(self, response):
        le = LinkExtractor(response)

