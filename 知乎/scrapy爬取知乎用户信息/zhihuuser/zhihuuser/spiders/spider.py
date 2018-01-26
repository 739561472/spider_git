# coding: utf-8
import json

from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuUser(Spider):
    name = 'zhihuuser'
    start_user = 'excited-vczh'
    include_follwees = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    include_user = 'allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    user_url = 'https://www.zhihu.com/api/v4/members/{}?include={}'
    user_followees_url = 'https://www.zhihu.com/api/v4/members/{uel_token}/followees?include={include}&offset={offset}&limit={limit}'

    def start_requests(self):
        yield Request(self.user_url.format(self.start_user, self.include_user), callback=self.parse_user)
        yield Request(self.user_followees_url.format(uel_token=self.start_user, include=self.include_follwees,
                                                     offset=20, limit=20), callback=self.parse_user_followee)

    def parse_user(self, response):
        item = UserItem()
        user_result = json.loads(response.text)
        for field in item.fields:
            if field in user_result.keys():
                item[field] = user_result.get(field)
        yield item
        yield Request(self.user_followees_url.format(uel_token=user_result['url_token'], include=self.include_follwees,
                                                     offset=20, limit=20), callback=self.parse_user_followee)

    def parse_user_followee(self, response):
        user_followee_result = json.loads(response.text)
        if isinstance(user_followee_result, dict) and 'data' in user_followee_result.keys():
            for user_followee in user_followee_result['data']:
                yield Request(self.user_url.format(user_followee['url_token'], self.include_user),
                              callback=self.parse_user)
        if 'paging' in user_followee_result.keys() and user_followee_result.get('paging').get('is_end') == False:
            next_page = user_followee_result.get('paging').get('next')
            yield Request(next_page, callback=self.parse_user_followee)

