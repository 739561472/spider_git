# -*- coding: utf-8 -*-

from time import sleep

import random
import pymongo
import requests
import http.cookiejar
import queue

from multiprocessing import Pool, Lock, Manager, Queue
from bs4 import BeautifulSoup
from config import *

client = pymongo.MongoClient()
db = client[MONGO_DB]

q = queue.Queue()

session = requests.session()
session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.1.2.3000 Chrome/55.0.2883.75 Safari/537.36'
headers = {
    "Host": "www.zhihu.com",
    "Origin": "https://www.zhihu.com/",
    "Referer": "http://www.zhihu.com/",
    'User-Agent': agent
}
try:
    session.cookies.load(ignore_discard=True)
except requests.HTTPError:
    print('cookie未加载')


def get_html(url):
    try:
        res = session.get(url=url, headers=headers).text
        sleep(random.choice([0.5, 0.3, 0.7]))
        bs0bj = BeautifulSoup(res, 'lxml')
        return bs0bj
    except requests.HTTPError as e:
        print(e, '网络连接错误！')


def get_father_topic_data(bs0bj):
    try:
        father_topic_list = []
        name = bs0bj.find('h1', {'class': 'zm-editable-content', 'data-disabled': '1'}).get_text()
        father_content = bs0bj.find('div', {'class': 'zm-side-section-inner parent-topic'}).findAll('a', {'class': 'zm-item-tag'})
        for s in father_content:
            father_topic_list.append(s.get_text())
        return father_topic_list, name
    except AttributeError:
        print('该话题没有父话题！')


def get_topic_token(bs0bj):
    try:
        children_content = bs0bj.find('div', {'class': 'zm-side-section-inner child-topic'}).findAll('a', {
            'class': 'zm-item-tag'
        })
        if children_content:
            for child_topic in children_content:
                if 'data-token' in child_topic.attrs:
                    data_token = child_topic.attrs['data-token']
                    get_ajax_data(data_token)
                    url = 'https://www.zhihu.com/topic/{data_token}/hot'.format(data_token=data_token)
                    q.put(url)
    except AttributeError:
        print('该话题没有子话题')


def get_ajax_data(data_token):
    ajax_url = 'https://www.zhihu.com/node/TopicProfileCardV2?params={"url_token":"'+data_token+'"}'
    bs0bj = get_html(ajax_url)
    name = bs0bj.find('span', {'class', 'name'}).get_text()
    content_value = bs0bj.findAll('span', {'class', 'value'})
    question_num = content_value[0].get_text()
    followers = content_value[2].get_text()
    topic = {
        'name': name,
        '问题数': question_num,
        '关注数': followers,
    }
    save_to_mongo(topic)


def save_to_mongo(topic_dict=None, father_topic=None, name=None):
    if topic_dict:
        if db[MONGO_TOPIC_TABLE].insert(topic_dict):
            print('话题插入成功！')
            return True
    else:
        if db[MONGO_TOPIC_TABLE].update({'name': name}, {'$set': {'父话题': father_topic}}):
            print('父话题插入成功！')
            return True


def controller(url):
    bs0bj = get_html(url)
    get_topic_token(bs0bj)
    if get_father_topic_data(bs0bj):
        father_topic_list, name = get_father_topic_data(bs0bj)
        save_to_mongo(father_topic=father_topic_list, name=name)


def main():
    start_url = 'https://www.zhihu.com/topic/19776749/hot'
    controller(start_url)
    while not q.empty():
        next_url = q.get()
        controller(next_url)


if __name__ == '__main__':
    main()
