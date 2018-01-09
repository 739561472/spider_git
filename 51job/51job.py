# -*- coding: utf-8 -*-
import random

__author__ = 'Hth'


import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from pymongo import MongoClient
from config import *
import re
import csv
import time

ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
      ]
start_url = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=020000%2C080200&keyword={keyword}&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'.format(keyword='Python%20%E7%88%AC%E8%99%AB')
client = MongoClient()
db = client[MONGO_DB]

class Tools:
    removeHtml = re.compile(r'.*?html$')
    removeLi = re.compile(r'<li.*?|\\t">')
    removeF = re.compile(r'<a href="|\\r|\\n')
    removeL = re.compile(r'">下一页</a></li>')
    removeClass = re.compile(r'class="bk">')
    removeC = re.compile(r'共|页，到第')
    def repalce(self,str):
        str = re.sub(self.removeHtml, '', str)
        str = re.sub(self.removeLi, '', str)
        str = re.sub(self.removeF, '', str)
        str = re.sub(self.removeL, '', str)
        str = re.sub(self.removeClass, '', str)
        str = re.sub(self.removeC, '', str)
        return str.strip()


class Job:
    def __init__(self,start_url):
        self.url = start_url
        self.tools = Tools()
        self.jobs = []
        self.urls = []
        self.number = 0

    def get_joburl(self,url = None):
        user_agent = random.choice(ua_list)
        headers = {'User_agent': user_agent}
        t = [1, 0.5, 0.8]
        try :
            if url == None:
                time.sleep(random.choice(t))
                res = urllib.request.Request(self.url,headers = headers)
                res = urllib.request.urlopen(res)
                self.parse_job_url(res)
            else:
                time.sleep(random.choice(t))
                req = urllib.request.Request(url,headers = headers)
                res = urllib.request.urlopen(req)
                self.parse_job_url(res)
        except urllib.error.HTTPError as e:
            print('网络错误:',e)

    def parse_job_url(self,res):
        bs0bj = BeautifulSoup(res, 'lxml')
        joblist = bs0bj.findAll('a', href=re.compile('^(http://jobs.51job.com)'))
        number = bs0bj.find('span', {'class': 'td'}).get_text()
        self.urls = bs0bj.findAll('li', {'class': 'bk', })
        self.number = self.tools.repalce(str(number))
        for job in joblist:
            if 'href' in job.attrs:
                job = job.attrs['href']
                job = self.tools.repalce(str(job))
                if job != '' and job != 'http://jobs.51job.com':
                    print(job)
                    self.get_job(job)
        self.next_page()

    def get_job(self,job):
        time.sleep(1)
        user_agent = random.choice(ua_list)
        headers = {'User_agent': user_agent}
        try:
            res = urllib.request.Request(job, headers=headers)
            res = urllib.request.urlopen(res)
            self.parse_job(res,job)
        except urllib.error.HTTPError as e:
            print(e)

    def parse_job(self,res,job):
        bs0bj = BeautifulSoup(res, "lxml")
        try:
            name = bs0bj.find('h1').get_text()
            adr = bs0bj.find('span', {'class': 'lname'}).get_text()
            salary = bs0bj.findAll('strong')
            company = bs0bj.find('p', {'class': 'cname'}).get_text()
            detial = bs0bj.findAll('span', {'class': 'sp4'})
            job_dict = {
                'name':name,
                'address':adr,
                'salary':salary[1].get_text(),
                'company':company,
                '经验':detial[0].get_text(),
                'degree':detial[1].get_text(),
                'url':job,
                '人数':detial[2].get_text()
            }
            print(job_dict)
            self.save_to_mongoDB(job_dict)
            # self.save_file(job_dict)
        except AttributeError as e:
            print(e)

    def save_to_mongoDB(self,job_dict):
        if db[MONGO_TABLE].insert(job_dict):
            print('插入成功！', job_dict)
            return True
        return False

    # def save_file(self,job_dict):
    #     csvfile = open('D:/pycharm/PycharmProjects/spder_demo/51job/job.txt','w', newline='')
    #     writer = csv.writer(csvfile)
    #     writer.writerow(job_dict)
    #     csvfile.close()

    def next_page(self):
        url = self.tools.repalce(str(self.urls[1]))
        if url != 'span>下一页</span></li':
            print('开始读取出下一页数据...')
            self.get_joburl(url)
        print('数据读取完毕！')

    def start(self):
        self.get_joburl()

job = Job(start_url)
url = job.start()
