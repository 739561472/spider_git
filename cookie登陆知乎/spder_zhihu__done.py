# -*- coding: utf-8 -*-
import requests
import http.cookiejar
import re
#import scrapy
from bs4 import BeautifulSoup

# from selenium import webdriver

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
except:
    print('cookie未加载')

def islogin():
    url = 'https://www.zhihu.com/settings/profile'
    login_code = session.get(url=url, headers=headers).status_code
    if login_code == 200:
        return True
    else:
        return False


def get_answer_html():
    url = 'https://www.zhihu.com/topic/20086364/hot'
    html = session.get(url, headers=headers)
    reg = r'<link itemprop="url" href="(.*?)">'
    answer_url = re.compile(reg)
    answer_list = re.findall(answer_url, html.text)
    return answer_list


def get_answer(answer_list):
    for url in answer_list:
        url = 'https://www.zhihu.com'+url
        answer_response = session.get(url, headers=headers)
        answer_params = answer_response.text
        reg = r'<p>(.*?)</p>'
        answer_data = re.findall(reg,answer_params)
        print(answer_data)


islogin()
answer_list = get_answer_html()
get_answer(answer_list)
