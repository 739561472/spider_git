# -*- coing:utf-8 -*-
import scrapy
from ..items import BooksItem
from scrapy.linkextractors import LinkExtractor

class BooksSpider(scrapy.Spider):
    name = 'books'

    #start_url = ['https://books.toscrape.com']

    def start_requests(self):
        yield scrapy.Request(12
            #'http://category.dangdang.com/cp01.03.41.00.00.00.html',
            #callback=self.parse_book,
            #headers={'user_agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'},
            #dont_filter = True
        )
    def parse_book(self, response):
        for sel in response.css('[sku]'):
            book = BooksItem()
            #书名在article>h3>a元素里面的title属性里
            book['name'] =  sel.xpath('./li/a/@title').extract_first()
            book['price'] = response.css('span.search_now_price::text').extract_first()
            print(book)
            yield book
        # 提取数据
        # 选用css选择器
        le = LinkExtractor(restrict_css='ul.fy li.next')
        links = le.extract_links(response)
        if links:
            next_url = links[0].url
            yield scrapy.Request(next_url, callback=self.parse())
        #     #提取下一页链接
        #     next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        #     if next_url:
        #         next_url = response.urljoin(next_url)
        #         yield scrapy.Request(next_url,callback=self.parse)