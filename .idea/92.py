# -*- coding: utf-8 -*-

__author__ = 'Hth'

import urllib.request
import urllib.error
#import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
headers = {'User_Agent':user_agent}


class HUPU:
    def __init__(self,baseurl):
        self.baseurl = baseurl
        #self.searchstr = searchstr
        self.tools = Tools()
        self.y = 0
        pass

    def get_pagenum(self,search_url):
        reg = r'<a herf="/search?q=%E4%B8%8D%E5%86%B7%E7%AC%91%E8%AF%9D&type=s_subject&sortby=postdate&page=/d">(/d+)</a>'
        pattern = re.compile(reg, re.S)
        pagenum = re.findall(pattern, str(search_url))
        print(pagenum)
        return pagenum


    def getSearch(self,next=None):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(5)
        driver.implicitly_wait(10)
        driver.get(self.baseurl)
        #assert "Python" in driver.title
        #elem = driver.find_element_by_name('q')
        #elem.send_keys('不冷笑话')
        #elem.send_keys(Keys.RETURN)
        n=0
        search_url = []
        while n<1:
            search_url.append(driver.page_source)
            next = driver.find_element_by_class_name('next')
            next.send_keys(Keys.RETURN)
            n+=1
            if n==1:
                driver.quit()
                break
        return search_url
        #normal_window = driver.current_window_handle
        # all_Handles = driver.window_handles
        # print(all_Handles)
        #driver.quit()


    def getJokeurl(self,search_url):
        reg_joke = r'"><a href="(.*?)">'
        joke_url = self.url_Re(reg_joke,str(search_url))
        #print(joke_url)
        return joke_url


    def getImg(self,joke_url):
        img_urls = []
        for url in joke_url:
            url = 'http://92.t9p.today/' + self.tools.repalce(url)
            #print(url)
            try:
                # request = urllib.request.Request(url)
                # res = urllib.request.urlopen(request)
                # res = res.read().decode('utf-8')
                #time.sleep(1)
                driver = webdriver.Chrome()
                #driver.set_page_load_timeout(5)
                driver.implicitly_wait(5)
                driver.get(url)
                res = driver.page_source
                driver.quit()
                reg_img = r'<img src="(.*?)" file="'
                img_url = self.url_Re(reg_img, str(res))
                if img_url ==None:
                    pass
                else:
                    img_urls.append(img_url)
               #print('1')
                #print(res)
            except:
                continue
        return img_urls

    def downloadImg(self,img_urls):
        print('正在下载图片.......')
        for n in img_urls:
            #print(n)
            for x in list(n):
                x=self.tools.repalce(x)
                x='http://92.t9p.today/'+x
                try:
                    urllib.request.urlretrieve(x,'D:\pycharm\PycharmProjects\91\%s.jpg' % self.y)
                    #print(x)#'+1')
                except:
                    continue
                    #time.sleep(1)
                self.y+=1

    def start(self):
        urls = self.getSearch()
        #print(url)
        #page_num= self.get_pagenum(url)
        #print(page_num)
        for url in urls:
            joke_url = self.getJokeurl(url)
            img_url = self.getImg(joke_url)
            self.downloadImg(img_url)
        print('图片下载完成！！！')
    def url_Re(self,reg,str):
        pattern = re.compile(reg,re.IGNORECASE)
        result = re.findall(pattern,str)
        return result
class Tools:
    removeDiv = re.compile(r'<div(.*?)>|</div>{1-5}|<div>')
    removeBR = re.compile(r'<br>{1-9}|<b>|</b>|<b></b>')
    removeA = re.compile(r'<a(.*?)>|</a>')
    removeFont = re.compile(r'<font(.*?)>|</font>')
    removeZi = re.compile(r'" />(.*)<img src="')
    remove = re.compile(r'" style="(.*?)|"(.*?)|:(.*?)')
    removeQ = re.compile(r'\s(.*?)')
    def repalce(self, str):
        str = re.sub(self.removeDiv, '', str)
        str = re.sub(self.removeBR, '', str)
        str = re.sub(self.removeA,'',str)
        str = re.sub(self.removeFont, '', str)
        str = re.sub(self.removeZi, '', str)
        str = re.sub(self.remove, '', str)
        str = re.sub(self.removeQ, '', str)
        return str.strip()

baseurl = 'http://92.t9p.today/forumdisplay.php?fid=19'
hupu_img = HUPU(baseurl)
#hupu_img.getSearch()
#input('输入抓取内容/关键字：')
joke_url = hupu_img.start()
