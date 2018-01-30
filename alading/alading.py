# coding: utf-8
__auther__ = 'Hth'

from config import *

import requests
import json
import pymongo


client = pymongo.MongoClient()
db = client[MONGO_DB]


def get_html(url, size=100, proxy=None):
    headers = {
                'Accept': 'application/json,text/javascript,*/*;q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep - alive',
                'Content-Length': '21',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Host': 'zhishuapi.aldwx.com',
                'Origin': 'http://www.aldzs.com',
                'Referer': 'http://www.aldzs.com/toplist',
                'User-Agent':'Mozilla/5.0(WindowsNT10.0;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36'
    }
    data = {
        'type': '1',
        'size': size,
        'token': ''
    }
    res = requests.post(url=url, headers=headers, data=data, proxies=proxy).text
    parse(res)


def parse(res):
    key_list = []
    data = json.loads(res)
    data_dict = data['data']
    try:
        for i in data_dict.keys():
            key_list.append(i)
        for i in range(len(key_list)):
            key = key_list[i]
            items = data_dict.get(key)
            for item in items:
                save_to_mongo(item, key)
    except AttributeError:
        for item in data_dict:
            save_to_mongo(item, 'xiaofaxian')


def save_to_mongo(item, MONGO_TABLE_USE):
    if db[MONGO_TABLE_USE].insert(item):
        print('插入成功')
        return True


def main():
    url = 'http://zhishuapi.aldwx.com/Main/action/Dashboard/Homepage/getNewsList'
    get_html(url)


if __name__ == '__main__':
    main()
