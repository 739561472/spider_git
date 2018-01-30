# coding : utf-8
# from pprint import pprint
import json
from time import sleep
from selenium import webdriver


cookies = {}
# 使用selenium打开Chrome或火狐必须得下载相应的webdriver，推荐使用PhantomJS无界面浏览器
driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\\chromedriver.exe')
url = 'https://mp.weixin.qq.com/'
driver.get(url)
driver.find_element_by_xpath('//input[@name="account"]').clear()
driver.find_element_by_xpath('//input[@name="account"]').send_keys('账号')  # 模拟输入账号
driver.find_element_by_xpath('//input[@name="password"]').clear()
driver.find_element_by_xpath('//input[@name="password"]').send_keys('你得密码')  # 模拟输入密码
driver.find_element_by_xpath('//a[@class="btn_login"]').click()  # 模拟鼠标点击
sleep(10)
cookie = driver.get_cookies()  # 拿到cookie
for item in cookie:
    cookies[item.get('name')] = item.get('value')  # 把cookie里没用的数据去掉，只要留下name跟value这两个值就够了
with open('cookie.txt', 'w+', encoding='utf-8') as f:
    f.write(json.dumps(cookies))  # 转换类型为str存储

#  拿到这个cookie之后就可以随便浪了-_-,不过现在访问貌似限速了--


