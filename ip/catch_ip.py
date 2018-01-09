# coding:utf-8

import random
import urllib.request
import urllib.error
from time import sleep

from pymongo import MongoClient

from config import *
import re

client = MongoClient()
db = client[MONGO_DB]

ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      ]
user_agent =random.choice(ua_list)

def get_ip(url):
    headers = {
        'User_agent': user_agent
    }
    try:
        req = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(req)
        content = response.read().decode('utf-8')
        parse_ip(content)
    except urllib.error.HTTPError as e:
        print(e)
    sleep(random.choice(range(1,3)))

def parse_ip(content):
    reg_ip = re.compile(r'<td data-title="IP">(.*?)</td>')
    reg_port = re.compile(r'<td data-title="PORT">(.*?)</td>')
    reg_time = re.compile(r'<td data-title="最后验证时间">(.*?)</td>')
    reg_type = re.compile(r'<td data-title="类型">(.*?)</td>')
    ip_list = re.findall(reg_ip, content)
    port_list = re.findall(reg_port, content)
    time_list = re.findall(reg_time,content)
    type_list = re.findall(reg_type, content)
    for n in range(len(ip_list)):
        result = {
            'ip': ip_list[n],
            'port': port_list[n],
            '最后验证时间': time_list[n],
            '类型': type_list[n]
        }
        save_to_mongo(result)

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('插入成功', result)
        return True
    return False

def main():
    #page = input('输入页数')
    for n in range(1, 50):#int(page)):
        url = 'https://www.kuaidaili.com/free/inha/{page}/'.format(page=n)#'http://www.xicidaili.com/nn/{page}'.format(page=n)
        get_ip(url)

if __name__ ==  '__main__':
    main()