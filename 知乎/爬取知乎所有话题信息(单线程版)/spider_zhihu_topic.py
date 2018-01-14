# -*- coding: utf-8 -*-

from time import sleep

import random
import pymongo
import requests
import http.cookiejar
import queue

from bs4 import BeautifulSoup
from config import *

client = pymongo.MongoClient()
db = client[MONGO_DB]
db_ip = client[MONGO_IP_DB]

q = queue.Queue()

session = requests.session()
# 读取之前存储的cookie文件
session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
]

try:
    session.cookies.load(ignore_discard=True)
except requests.HTTPError:
    print('cookie未加载')


def get_headers():
    user_agent = random.choice(ua_list)

    headers = {
        "Host": "www.zhihu.com",
        "Origin": "https://www.zhihu.com/",
        "Referer": "http://www.zhihu.com/",
        'User-Agent': user_agent
    }
    return headers


def get_html(url, proxy=None):
    try:
        res = session.get(url=url, headers=get_headers(), proxies=proxy, timeout=5).text
        sleep(0.3)
        bs0bj = BeautifulSoup(res, 'lxml')
        session.close()
        return bs0bj
    except (requests.ConnectionError, requests.ConnectTimeout, requests.HTTPError, requests.Timeout):
        print('网络连接错误！')


def get_father_topic_data(bs0bj):
    father_topic_list = []
    try:
        name = bs0bj.find('h1', {'class': 'zm-editable-content', 'data-disabled': '1'}).get_text()
        father_content = bs0bj.find('div', {'class': 'zm-side-section-inner parent-topic'}).findAll('a', {
            'class': 'zm-item-tag'})
        for s in father_content:
            father_topic_list.append(s.get_text())
        return father_topic_list, name
    except AttributeError:
        print('该话题没有父话题！')


def get_topic_token(bs0bj):
    children_content = []
    try:
        children_content = bs0bj.find('div', {'class': 'zm-side-section-inner child-topic'}).findAll('a', {
            'class': 'zm-item-tag'
        })
    except AttributeError:
        print('该话题没有子话题')
    if children_content:
        for child_topic in children_content:
            if 'data-token' in child_topic.attrs:
                data_token = child_topic.attrs['data-token']
                get_ajax_data(data_token)
                url = 'https://www.zhihu.com/topic/{data_token}/hot'.format(data_token=data_token)
                q.put(url)


def get_ajax_data(data_token):
    ajax_url = 'https://www.zhihu.com/node/TopicProfileCardV2?params={"url_token":"' + data_token + '"}'
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
    # 将拿到数据存储至mongoDB
    if topic_dict:
        if db[MONGO_TOPIC_TABLE].insert(topic_dict):
            print('话题插入成功！')
            return True
    else:
        if db[MONGO_TOPIC_TABLE].update({'name': name}, {'$set': {'父话题': father_topic}}):
            print('父话题插入成功！')
            return True


def controller(url, ip=None):
    # 控制各个函数执行顺序
    bs0bj = get_html(url, ip)
    get_topic_token(bs0bj)
    if get_father_topic_data(bs0bj):
        father_topic_list, name = get_father_topic_data(bs0bj)
        save_to_mongo(father_topic=father_topic_list, name=name)


# def working():
#     next_url = q.get()
#     controller(next_url)
#     q.task_done()


def main():
    ip_list = []
    n = 0
    queryArgs = {}
    projectionfileds = {'ip': True}
    for i in range(4):
        # 暂时不清楚怎么顺序查找，由于存储是没有设置id1234等等
        ip = db_ip[MONGO_IP_TABLE].find_one_and_delete(queryArgs, projection=projectionfileds)
        ip = {'http': ip['ip'],
              'https': ip['ip']}
        ip_list.append(ip)
    start_url = 'https://www.zhihu.com/topic/19776749/hot'
    controller(start_url)
    # 判断队列是否为空
    while not q.empty():
        # 从队列中取url
        next_url = q.get()
        if n >= 500:
            ip = random.choice(ip_list)
            controller(next_url, ip)
        elif n >= 1000:
            n = 0
        else:
            controller(next_url)
        n += 1
        # for i in range(2):
        #     t = threading.Thread(target=working)
        #     t.setDaemon(True)
        #     t.start()


if __name__ == '__main__':
    main()
