# coding:utf-8
# __auther__ = 'Hth'

import re
import time
import random
from urllib.parse import quote

from pymongo import MongoClient
from bs4 import BeautifulSoup

import requests

from region import captcha
from region.config import *


# 取client对象
client = MongoClient()
# 设置数据库名
db_ip = client[MONGO_IP_DB]
db = client[MONGO_DB]


# 获得网页内容
def get_html(url, proxy=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    try:
        # 使用get函数时设置代理ip，并设置最长时间3秒
        response = requests.get(url, headers=headers, proxies=proxy, timeout=3).text
        time.sleep(0.5)
        return response
    except requests.HTTPError as e:
        print('网络错误', e)
    except requests.exceptions.ConnectTimeout as e:
        print('该ip网络延迟过高', e)


# 调用get_html将网页内容传入处理函数parse取出city列表
def get_city(url):
    response = get_html(url)
    city_name = parse(response, 0)
    if city_name[0] == 1:
        return interrupt(city_name, url, i=1), url
    else:
        return city_name


# 同理取出region列表
def get_region(city_english_name, ip=None):
    url = 'http://{city}.fangjia.com/zoushi/'.format(city=city_english_name)
    response = get_html(url, ip)
    region_name = parse(response, 1)
    if region_name[0] == 1:
        return interrupt(region_name, url, i=1), url
    else:
        return region_name, url


# 取出block列表
def get_block(region, url, ip):
    # 将region进行url编码，加到原url后面
    url = url+quote(region)
    response = get_html(url, ip)
    block_name = parse(response, 2)
    # 由于存在区域无板块情况，parse返回为空，所以先判断block_name是否存在，防止存入数据库和判断是否等于1时出现异常
    if block_name:
        if block_name[0] == 1:
            return interrupt(block_name, url, i=2)
        else:
            return block_name


# 网页处理函数
def parse(res, i):
    # 取bs4对象
    bs0bj = BeautifulSoup(res, 'lxml')
    # 根据传入信号量i判断，case 为验证码处理，0为city列表处理，1为region列表处理，2为block列表处理
    msg = ''
    captcha_item = bs0bj.find('script')
    if str(captcha_item) == '<script src="http://static.fangjia.com/stc/js/jquery-1.8.3.js"></script>':
        while msg != 'success':
            msg = captcha.handler_captcha()
        return ['1']
    if i == 0:
        city_name = []
        city_content = bs0bj.find('div', {'class': 'tab_content', 'id': 'moreCity'})
        city_tag = city_content.findAll('a')
        for city in city_tag:
            # 由于获取region列表url需要城市拼音简称，所以一并取出
            city_dict = {
                'name': city.get_text(),
                # tag.attrs['class']为获取属性内容的函数
                'english_name': city.attrs['name']
            }
            city_name.append(city_dict)
        return city_name
    elif i == 1:
        region_name = []
        region_content = bs0bj.find('div', {'class': 'noteText dn', 'id': 'regionDiv'})
        region_tag = region_content.findAll('a')
        for region in region_tag:
            # 调用replace函数，过滤空格与换行符
            region = replace(region.get_text())
            if region != '不限':
                region_name.append(region)
        return region_name
    elif i == 2:
        block_name = []
        try:
            block_content = bs0bj.find('div', {'class': 'noteText dn', 'id': 'blockDiv'})
            block_tag = block_content.findAll('a')
            for block in block_tag:
                block = replace(block.get_text())
                if block != '不限':
                    block_name.append(block)
            return block_name
        except AttributeError:
            print('该区域无板块!')
    else:
        print('识别码有误！')


# 识别完验证码后，重新读取上一个url的内容
def interrupt(url, ip=None, i=None):
    response = get_html(url, ip)
    name = parse(response, i)
    return name


# 连接数据库并存储数据
def db_connection(i=1, data=None, parents=None, city_english_name=None):
    ip_list = []
    if i == 0:
        for i in range(5, 10):
            # 取第5到第10个ip
            item = db_ip[MONGO_IP_TABLE].find_one({'count': i})
            ip_list.append({'http': item['ip']})
        return ip_list
    else:
        if city_english_name:
            # 用父连接结构插入树的节点
            if db[MONGO_TABLE].insert({'name': data, 'city_english_name': city_english_name, 'path': parents,
                                       '两年房价数据': ''}):
                print('插入成功！！！')
                return True
        else:
            if db[MONGO_TABLE].insert({'name': data, 'path': parents, '两年房价数据': ''}):
                print('插入成功！！！')
                return True


def replace(replace_str):
    # 过滤换行符\n和空格\s，+号代表至少一个
    remove = re.compile(r'\n|\s+')
    replace_str = re.sub(remove, '', replace_str)
    return replace_str


def tree(city, ip):
    # 将城市，区域，板块以树形结构存储进mongodb
    city_name = city['name']
    city_english_name = city['english_name']
    db_connection(data=city_name, city_english_name=city_english_name)
    # 父节点存储城市名
    region_name, url = get_region(city_english_name=city_english_name, ip=ip)
    # city_dict = {
    #     '房价': ''
    # }
    for region in region_name:
        # 以城市名为父节点存储区域
        db_connection(data=region, parents=city_name)
        # region_dict = {
        #     '房价': ''
        # }
        block_name = get_block(region, url, ip)
        if block_name:
            for block in block_name:
                # 以区域名为父节点存储板块
                parents = city_name+'-'+region
                db_connection(data=block, parents=parents)
                # block_dict = {
                #     '房价': ''
                # }
    #             region_dict[block] = block_dict
    #     city_dict[region] = region_dict
    # total = {
    #     city_name: city_dict
    # }
    # 以上是构建字典形式的数据，因为目前用不到所以注释


def main():
    url = 'http://abazhou.fangjia.com/'
    # res = get_html('http://hz.fangjia.com/validate')
    # 取出代理ip列表
    # ip_list = db_connection(0)
    # 令list[0]为空，这样可以默认使用本机ip
    # ip_list[0] = None
    # 取出city列表
    city_name_dict = get_city(url)
    for city in city_name_dict:
        # 若想使用代理ip，则取消相关代理ip代码的注释即可
        # ip = random.choice(ip_list)
        ip = None
        tree(city, ip)


if __name__ == '__main__':
    main()
