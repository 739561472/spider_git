# coding: utf-8

from scrapy import Spider, Request


class JobsSpider(Spider):
    name = 'bossjob'
    url = 'https://www.zhipin.com{city_page}'
    start_city_page = '/c101210100/h_101210100/?query=python&page=1'

    def start_requests(self):
        yield Request(self.url.format(city_page=self.start_city_page), callback=self.parse_job)

    def parse_job(self, response):
        # print(response.text)
        selector_list = response.xpath('//div[@class="job-list"]/ul/li/div[@class="job-primary"]')
        for job_content in selector_list:
            job_id = job_content.xpath('.//div[@class="info-primary"]/h3/a/@data-jid').extract()
            url = job_content.xpath('.//div[@class="info-primary"]/h3/a/@href').extract()
            job_name = job_content.xpath('.//div[@class="info-primary"]/h3/a/div[@class="job-title"]/text()').extract()
            salary = job_content.xpath('.//div[@class="info-primary"]/h3/a/span/text()').extract()
            job_detials = job_content.xpath('.//div[@class="info-primary"]/p/text()').extract()
            company = job_content.xpath('.//div[@class="info-company"]/div/h3/a/text()').extract()
            company_detials = job_content.xpath('.//div[@class="info-company"]/div/p/text()').extract()
            time = job_content.xpath('.//div[@class="info-publis"]/p/text()').extract()
            item = {
                '_id': job_id[0],
                'job_name': job_name[0],
                'url': url[0],
                'salary': salary[0],
                'region': job_detials[0],
                'experice': job_detials[1],
                'grades': job_detials[2],
                'company': company[0],
                'company_detials': company_detials,
                'time': time[0]
            }
            yield item
        next_page = response.xpath('//div[@class="page"]/a[@ka="page-next"]/@href').extract()
        yield Request(self.url.format(city_page=next_page[0]), callback=self.parse_job)


