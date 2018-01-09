#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'Hth'

import urllib.request
import re


def saveFile(data):
    path = ('D:/pycharm/PycharmProjects/spder_demo/output/qiushi.text')
    f = open(path, 'wb')
    f.write(data)
    f.close()

url = 'http://www.qiushibaike.com/'
user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'

headers = {'User-Agent': user_agent}

req = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(req)

content = response.read().decode('utf-8')
    # 使用compile将正则表达式编译并存入一个pattern变量中
    # 注：这里使用了四个正则额表达式，每一个表达式获取一个想要的信息
pattern = re.compile(r'<h2>(.*?)</h2>.*?'+'<div.*?class="content">(.*?)<!.*?'+'<div.*?class="stats".*?class="number">(.*?)</i>.*?'+'<span.*?class="dash".*?class="number">(.*?)</i>.*?',re.S)
    # 使用findall方法按re查找，findall返回的是一个列表
items = re.findall(pattern,content)
    # 使用for循环遍历列表中的元素并将它们打印出来
for item in items:
    data = '发布人：'+item[0]+'\n','段子内容：'+item[1]+'\n','点赞数:'+item[2]+'\n','评论数:'+item[3]+'\n'
    print(data)
