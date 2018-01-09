# encoding: utf-8
import json
import random
from time import sleep

import requests
from bs4 import BeautifulSoup

__author__ = 'Hth'

ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      ]

def get_header():
    user_agent = random.choice(ua_list)
    header ={
                "Accept":'application/json,text/javascript, */*; q=0.01',
                "Accept - Encoding": 'gzip,deflate,br',
                'Accept - Language': 'zh-CN,zh;q=0.9',
                'Connection':'keep-alive',
                'Content - Length':'44',
                'Content - Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Cookie': '_ga=GA1.2.326732678.1513822908; user_trace_token=20171221102147-b20c06ae-e5f5-11e7-9df7-5254005c3644; LGUID=20171221102147-b20c0e03-e5f5-11e7-9df7-5254005c3644; _gid=GA1.2.467276443.1515394827; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=fa44af58d459b4188de459f58d61a83648d5ccfae4c77c7c; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAACDBABJB8BF8EAB6D4B805D025BA5A458B48DE7B; _gat=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514363237,1515394827,1515402576,1515468554; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515468554; LGSID=20180109112913-43a47721-f4ed-11e7-a022-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_; LGRID=20180109112913-43a47870-f4ed-11e7-a022-5254005c3644; SEARCH_ID=0d3280e744924e47a31d2c740be4c988',
                'Host': 'www.lagou.com',
                'Origin': 'https://www.lagou.com',
                'Referer': 'https://www.lagou.com/jobs/list_Python%20%E7%88%AC%E8%99%AB?px=default&city=%E6%9D%AD%E5%B7%9E',
                'User_agent': user_agent,
                'X-Anit-Forge-Code': '0',
                'X-Anit-Forge-Token': 'None',
                'X-Requested-With':'XMLHttpRequest',
            }
    #print(header)
    return header

def parse_page(res,url):
    bsobj = BeautifulSoup(res.text, 'lxml')
    try:
        job_company = bsobj.find('div', {'class': 'company'}).get_text()
        job_name = bsobj.find('span', {'class': 'name'}).get_text()
        job_request = bsobj.find('dd', {'class': 'job_request'}).get_text()
        job_advantage = bsobj.find('dd', {'class': 'job-advantage'}).get_text()
        job_bt = bsobj.find('dd', {'class': 'job_bt'}).get_text()
        work_addr = bsobj.find('div', {'class':'work_addr'}).get_text().strip("\\n")
        next_url_content = bsobj.find('a',{'rel':'nofollow','class':'checkAll'}).attrs['href']
        dict = {
            'company': job_company,
            'name': job_name,
            'request': job_request,
            'advantage': job_advantage,
            'bt': job_bt,
            'work_addr': work_addr,
            'job_url': url
        }
        print(dict)
        # save_data(dict)
        #get_next_url(next_url_content)
    except AttributeError:
        print('当前页面缺少某些数据，但无较大影响！')

def parse_next_url(res):
    bsobj = BeautifulSoup(res.text, 'lxml')
    for next_content in bsobj.findAll('a', {'class': 'position_link'}):
        if 'href' in next_content.attrs:
            next_url = next_content.attrs['href']
            print(next_url)
            get_page(next_url)
def get_context(url):
    data = {
        'first': 'false',
        'pn': '1',
        'kd': 'Python 爬虫'
    }
    headers = get_header()
    res = requests.post(url=url, headers=headers, data=data)
    #res = requests.request(method=requests.post,url= url)
    #3print(res.text)
    #numbers = res.json()
    result = json.loads(res.text)
    #parse_page(result)
def get_page(url):
    res = requests.get(url,headers = get_header(),)
    #sleep(0.2)
    parse_page(res,url)

# def get_next_url(next_url_content):
#     res = requests.get(next_url_content, headers=header)
#     parse_next_url(res)

def main():
    start_url = 'https://www.lagou.com/jobs/positionAjax.json'#?px=default&city=%E6%9D%AD%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0'
    #start_url = 'https://www.lagou.com/jobs/list_{job_name}?px=default&city={job_city}#filterBox'.format(job_name = 'python 爬虫',job_city = '杭州')
    get_context(start_url)

if __name__ ==  '__main__':
    main()
