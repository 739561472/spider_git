# encoding : utf-8
import json
import random
from prettytable import PrettyTable
import re
import requests
from urllib.parse import quote

ua_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        ]


def get_headers():
    # 定制请求头
    user_agent = random.choice(ua_list)
    headers['User-Agent'] = user_agent
    return headers


url = 'https://sjipiao.fliggy.com/searchow/search.htm?_ksTS=1517555514866_177&depCityName={city_begin}&arrCityName={city_arr}&depDate={datetime}&searchSource=99&needMemberPrice=true&_input_charset=utf-8&ua=090%23qCQXu4X2X2wXPXi0XXXXXQkOIou1HUh%2BfQJ7O6muAGBvzHP7cPZG%2BSiO3H01j99s%2F4QXU6hnXXa3HoQCh9kXCx73Oh5eG2XPHYVyrFhnLXj3HoDIh9k41Y73IvlkXvXuLWQ5HfDjH4QXaPjPiPgQaXFjwvQXuN%2Fcu4iW0iPfGh%2FK2zYGPENxm8HgR5tGQJm%2FXvXuZW4R4tG0q4QXius%2BSbQEXvXQceniiv%3D%3D&openCb=false'
#data get
headers = {
    'GET /searchow/search.htm?_ksTS=1517555514866_177&depCityName=%E4%B8%8A%E6%B5%B7&arrCityName=%E6%B7%B1%E5%9C%B3&depDate=2018-03-04&searchSource=99&needMemberPrice=true&_input_charset=utf-8&ua=090%23qCQXu4X2X2wXPXi0XXXXXQkOIou1HUh%2BfQJ7O6muAGBvzHP7cPZG%2BSiO3H01j99s%2F4QXU6hnXXa3HoQCh9kXCx73Oh5eG2XPHYVyrFhnLXj3HoDIh9k41Y73IvlkXvXuLWQ5HfDjH4QXaPjPiPgQaXFjwvQXuN%2Fcu4iW0iPfGh%2FK2zYGPENxm8HgR5tGQJm%2FXvXuZW4R4tG0q4QXius%2BSbQEXvXQceniiv%3D%3D HTTP/1.1'
    'Host': 'sjipiao.fliggy.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': ' 1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'cna=0XrPEgE80hgCAXHh0YeKsMPX; hng=CN%7Czh-CN%7CCNY%7C156; t=372abd607e1072a614bd71aee198c724; tracknick=%5Cu68A611132; _tb_token_=7b7b7335bc637; cookie2=14fe2f48b08e68d279eb966a74d28cd6; UM_distinctid=161313fd697451-0b7d2a62818168-3c604504-1fa400-161313fd698847; CNZZDATA30066717=cnzz_eid%3D244520337-1516948226-https%253A%252F%252Fwww.fliggy.com%252F%26ntime%3D1517551115; isg=BJycK-EHKttjW94Z9iW_zZ8mbbqOvUFDfzhNhnafqgd4wTxLniUQzxJbJSk5yXiX',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_page(city_begin, city_arr, datetime):
    res = requests.get(url.format(city_begin=quote(city_begin), city_arr=quote(city_arr), datetime=datetime),
                       headers).text
    reg = re.compile(r'\(|\)|;')
    result = json.loads(re.sub(reg, '', res)).get('data')
    return result
    # data clean


def parse(result):
    aircodeNameMap = result.get('aircodeNameMap')
    airportMap = result.get('airportMap')
    for item in result.get('flight'):
        price = item.get('cabin').get('bestPrice')
        discount = item.get('cabin').get('bestDiscount')
        air_company = aircodeNameMap.get(item.get('airlineCode'))
        air_code = item.get('flightNo')
        airport_arr = airportMap.get(item.get('arrAirport'))
        airport_beg = airportMap.get(item.get('depAirport'))
        arr_time = item.get('arrTime')
        beg_time = item.get('depTime')
        flight_type = item.get('flightType')
        pt = PrettyTable(["航班信息", "起降时间", "起抵机场", "最低价格"], border=True)
        pt.add_row([(air_company, air_code), beg_time, airport_beg, ''])
        pt.add_row([flight_type, arr_time, airport_arr, (price, str(discount)+'折')])
        pt.reversesort = True
        print(pt)
        if price <= 500 and air_company is not '春秋航空':
            return pt


def main():
    city_begin = input('请输入出发地：')
    city_arr = input('请输入目的地：')
    datetime = input('请输入时间：')
    result = get_page(city_begin, city_arr, datetime)
    pt = parse(result)


if __name__ == '__main__':
    main()
