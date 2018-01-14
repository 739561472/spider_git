# coding:utf-8

import random
from time import sleep

import requests
from pymongo import MongoClient

from config import *
from bs4 import BeautifulSoup
import re

client = MongoClient()
db = client[MONGO_DB]

ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
      ]
user_agent = random.choice(ua_list)


def get_ip(url):
    headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': user_agent,
            'Hosts': 'hm.baidu.com',
            'Referer': 'http://www.xicidaili.com/nn',
            'Connection': 'keep-alive'
    }
    try:
        response = requests.get(url=url, headers=headers)
        parse_ip(response.text)
    except requests.HTTPError as e:
        print(e)
    sleep(random.choice(range(1, 3)))


def parse_ip(response):
    ip_list = re.findall('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?(\d{2,6})', response, re.S)
    for li in ip_list:
        ip = li[0] + ':' + li[1]
        ip_dict = {
                    'ip': ip
                   }
        save_to_mongo(ip_dict)


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('插入成功', result)
        return True
    return False


def main():
    for n in range(1000, 2364):
        url = 'http://www.xicidaili.com/nn/{page}'.format(page=n)
        get_ip(url)


if __name__ == '__main__':
    main()
