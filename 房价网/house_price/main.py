# coding:'utf-8'
import json
from urllib import parse

import pymongo
import requests
import time


from region.config import MONGO_DB, MONGO_TABLE

client = pymongo.MongoClient()
db = client[MONGO_DB]


def db_connection(i=None, data=None, name=None):
    if i == 0:
        name_list = db[MONGO_TABLE].find()
        return name_list
    else:
        db[MONGO_TABLE].update({'name': name}, {'$set': data})


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
        response = requests.get(url, headers=headers, proxies=proxy, timeout=3)
        time.sleep(0.5)
        return response.text
    except requests.HTTPError as e:
        print('网络错误', e)
    except requests.exceptions.ConnectTimeout as e:
        print('该ip网络延迟过高', e)


def create_url(default_city_name, city_english_name='', region='', block='', keyword='', district_name=''):
    query_string_parameters = {
        'defaultCityName': default_city_name,
        'districtName': district_name,
        'region': region,
        'block': block,
        'keyword': keyword
    }
    _url = 'http://{city_english_name}.fangjia.com/trend/year2Data?'.format(city_english_name=city_english_name)
    url_data = parse.urlencode(query_string_parameters)
    url = _url+url_data
    return url


def select_content(name_dict):
        default_city_name = name_dict['name']
        path = name_dict['path']
        if path is None:
            city_english_name = name_dict['city_english_name']
            return create_url(default_city_name, city_english_name=city_english_name)
        elif '-' in path:
            name_list = path.split('-')
            name = db[MONGO_TABLE].find_one({'name': name_list[0]})
            city_english_name = name['city_english_name']
            return create_url(default_city_name=name_list[0], city_english_name=city_english_name, region=name_list[1],
                              block=default_city_name)
        else:
            name = db[MONGO_TABLE].find_one({'name': path})
            city_english_name = name['city_english_name']
            return create_url(default_city_name=path, city_english_name=city_english_name,region=default_city_name)


def transfer_time(time_str):
    time_str = time_str/1000.0
    time_attr = time.localtime(time_str)
    time_date = time.strftime('%Y-%m-%d', time_attr)
    return time_date


def collate_data(items):
    data_list = []
    for item in items:
        time_date = transfer_time(item[0])
        data_dict = {
            '日期': time_date,
            '房价': item[1]
        }
        data_list.append(data_dict)
    return data_list


def main():
    name_list = db_connection(0)
    # print(name_list)
    for name_dict in name_list:
        print(name_dict)
        name = name_dict['name']
        url = select_content(name_dict)
        print(url)
        # name = '阿坝州'
        # url = 'http://abazhou.fangjia.com/trend/yearData?defaultCityName=%E9%98%BF%E5%9D%9D%E5%B7%9E&
        # districtName=&region=&block=&keyword='
        content = json.loads(get_html(url))
        print(content)
        if content['title'] == '':
            db_connection(data={"两年房价数据": '这地方经济不发达，还没有房价数据'}, name=name)
        else:
            if 'series' in content.keys():
                data = content['series'][0]
                items = data['data']
                data_list = collate_data(items)
            else:
                items = content['data']
                data_list = collate_data(items)
            data = {'两年房价数据': data_list}
            db_connection(data=data, name=name)


if __name__ == '__main__':
    main()
