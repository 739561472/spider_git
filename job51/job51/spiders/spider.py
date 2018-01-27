# coding : utf-8

from scrapy import Spider, Request
# from job51.items import Job51Item


class JobsSpider(Spider):

    name = 'job51'
    url = 'http://search.51job.com/list/020000%252C080200,000000,0100%252C2500,32%252C01%252C38%252C40,9,99,%2B,2,{page}.html?{include}'
    include = 'lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    page = 1

    def start_requests(self):
        yield Request(self.url.format(page=self.page, include=self.include), callback=self.parse_job)

    def parse_job(self, response):
        # item = Job51Item()
        selector_list = response.xpath('//div[@class="dw_table"]/div[contains(@class,"el")]')
        for job_item in selector_list:
            job_name = job_item.xpath('.//p/span/a/text()').extract()
            url = job_item.xpath('.//p/span/a/@href').extract()
            company = job_item.xpath('.//span[@class="t2"]/a/@title').extract()
            region = job_item.xpath('.//span[@class="t3"]/text()').extract()
            salary = job_item.xpath('.//span[@class="t4"]/text()').extract()
            date = job_item.xpath('.//span[@class="t5"]/text()').extract()
            if len(job_name) == 1:
                item = {
                    'job_name': ''.join(job_name),
                    'url': ''.join(url),
                    'company': ''.join(company),
                    'region': ''.join(region),
                    'salary': ''.join(salary),
                    'date': ''.join(date)
                }
                yield item
        self.page += 1
        if self.page <= 1479:
            yield Request(self.url.format(page=self.page, include=self.include), callback=self.parse_job)
