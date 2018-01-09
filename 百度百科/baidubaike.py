#coding :# -*- coding: utf-8 -*-

__author__ = 'Hth'


import urllib.request
from bs4 import BeautifulSoup
import re
import csv
import time


user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
headers = {'User_agent':user_agent}
a = 'http://search.51job.com/list/020000%252C080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='


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
    def __init__(self,a):
        self.url = a
        self.tools = Tools()
        self.jobs = []
        self.names = []
        self.adrs = []
        self.salarys = []
        self.companys = []
        self.detials = []
        self.requirments = []
        self.sign = 0
        self.number = 0

    def get_joburl(self,url = None):
        if url == None:
            time.sleep(0.5)
            res = urllib.request.Request(self.url,headers = headers)
            res = urllib.request.urlopen(res)
        else:
            time.sleep(0.5)
            res = urllib.request.Request(url,headers = headers)
            res = urllib.request.urlopen(res)
        self.bs0bj = BeautifulSoup(res,"lxml")
        joblist = self.bs0bj.findAll('a',href = re.compile('^(http://jobs.51job.com)'))
        number = self.bs0bj.find('span',{'class':'td'}).get_text()
        self.number = self.tools.repalce(str(number))
        for job in joblist:
            #print(job)
            if 'href' in job.attrs:
                job = job.attrs['href']
                job = self.tools.repalce(str(job))
                if job !='' and job!='http://jobs.51job.com':
                    self.jobs.append(job)

    def get_job(self):
        for job in self.jobs:
            time.sleep(0.5)
            res = urllib.request.Request(job, headers=headers)
            res = urllib.request.urlopen(res)
            bs0bj = BeautifulSoup(res, "lxml")
            name = bs0bj.find('h1').get_text()
            adr = bs0bj.find('span',{'class':'lname'}).get_text()
            salary = bs0bj.findAll('strong')
            company = bs0bj.find('p',{'class':'cname'}).get_text()
            detial = bs0bj.find('span',{'class':'sp4'}).get_text()
            requirment = bs0bj.find('div',{'class':'bmsg job_msg inbox'}).get_text()
            self.names.append(name)
            self.adrs.append(adr)
            self.salarys.append(salary[1].get_text())
            self.companys.append(company)
            self.detials.append(detial)
            self.requirments.append(requirment)
            #print(company)

    def savefile(self):
        csvFile = open('D:/pycharm/PycharmProjects/spder_demo/51job/job.csv','w', newline='')
        writer = csv.writer(csvFile)
        l = len(self.names)
        # try:
        writer.writerow(['name','address','salarys','companys','detials','工作要求'])

        for n in range(l-1):
            try:
                print('+1s')
                writer.writerow([str(self.names[n]),str(self.adrs[n]),str(self.salarys[n]),str(self.companys[n]),str(self.detials[n]),str(self.requirments[n])])
            except:
                continue

        csvFile.close()
        print('一页数据写入完成，即将开始下一页')

    def next_page(self):
        urls = self.bs0bj.findAll('li',{'class':'bk',})
        url = self.tools.repalce(str(urls[1]))
        print('开始读取出下一页数据...')
        return url
        # if self.url != None:
        #     self.get_joburl()
        # else:
        #     print('下载完毕！')

    def start(self):
        n=0
        self.get_joburl()
        self.get_job()
        self.savefile()
        url = self.next_page()
        while n<int(self.number):
            try:
                print(n)
                self.get_joburl(url)
                self.get_job()
                self.savefile()
                url = self.next_page()
                n+=1

            except:
                break

job = Job(a)
url = job.start()
