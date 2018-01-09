# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# import re
#import scrapy
#url = 'https://i10.hoopchina.com.cn/hupuapp/bbs/831/18283831/thread_18283831_20171210125752_s_219267_h_735px_w_414px1027959966.jpeg'
# driver = webdriver.Chrome()
# driver.implicitly_wait(7)
# driver.get(url)
# js = "var q=document.documentElement.scrollTop=100000"
# driver.execute_script(js)
# time.sleep(3)
# res = driver.page_source
# driver.quit()
# reg_img = r'<img src="(.*?)" data'
# pattern = re.compile(reg_img)
# result = re.findall(pattern, str(res))
# b = 'CDwindow-(EFA94FEC14BF5339D55DC1DABCE7E259)'
# next_page = driver.find_elements_by_tag_name('<a herf="/search?q=%E4%B8%8D%E5%86%B7&page=1">')
# next_page.send_keys(Keys.RETURN)
#print(result)
#
#img_url.append(self.url_Re(reg_img,str(res