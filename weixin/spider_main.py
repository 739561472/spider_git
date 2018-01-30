# coding:utf-8
import json
import random
import re
import requests

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Host': 'mp.weixin.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}
with open('cookie.txt', 'r+') as f:
    cookie = f.read()
cookies = json.loads(cookie)
token_url = requests.get('https://mp.weixin.qq.com', cookies=cookies).url
token = re.findall(r'token=(\d+)', str(token_url))[0]


def get_contents(query):
    params = get_params('search_biz', query)
    url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    try:
        response = requests.get(url=url, cookies=cookies, params=params).content
        response = json.loads(response)
        fake_id = response.get('list')[0].get('fakeid')
        return fake_id
    except Exception as e:
        print('网络连接错误', e)


def get_params(action, query=None, fake_id=None, begin=0):
    params = {
        'action': '{action}'.format(action=action),
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'begin': begin,
        'count': '5',
        'query': query
    }
    if fake_id:
        params['fakeid'] = fake_id
        params['type'] = 9
    return params


def get_article_contents(fake_id, begin=0):
    params = get_params('list_ex', fake_id=fake_id, begin=begin)
    url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    try:
        response = requests.get(url=url, cookies=cookies, params=params, headers=headers).content
        return response, begin
    except Exception as e:
        print('网络连接错误', e)


def parse_article_url(response):
    response = json.loads(response)
    num = response.get('app_msg_cnt')
    for item in response.get('app_msg_list'):
        url = item.get('link')
        with open('artile.txt', 'w+') as f:
            f.write(str(url).join('\n'))
    return num


def main():
    query = input('输入公众号名称：')
    fake_id = get_contents(query)
    while True:
        response, begin = get_article_contents(fake_id)
        num = parse_article_url(response)
        if num - begin <= 6:
            break


if __name__ == '__main__':
    main()
