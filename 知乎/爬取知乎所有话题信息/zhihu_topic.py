# coding:utf-8
# import http.cookiejar
import json
import random
import threading
from queue import Queue
from time import sleep
from pymongo import MongoClient,errors
import requests

from config import *

q = Queue()
lock = threading.Lock()
client = MongoClient()
db = client[MONGO_DB]
session = requests.session()
# 读取之前存储的cookie文件
# session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')
# try:
#     session.cookies.load(ignore_discard=True)
# except requests.HTTPError:
#     print('cookie未加载')


class ZhihuTopicTask:
    def __init__(self, lock, ip=None):
        self.save_db = db[MONGO_TABLE]# db[MONGO_TOPIC_TABLE]
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'authorization': 'Bearer 2|1:0|10:1516431394|4:z_c0|92:Mi4xeXhiTUFRQUFBQUFBUUlJd0tYN1hEQ1lBQUFCZ0FsVk5JalpRV3dCbmo0WWVaNEgxWUtHcXRCZVBrX0pCLUNtTVdR|bd8d7d04b8c5ff3d72caa18d158a0605cf445f81b871060c28813e31c71ec3ab',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_zap=0ad13437-1f6b-4d51-90e5-5fa9b3ee60ea; d_c0="AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE=|1513399908"; q_c1=5ddb74d22f8249cf84ebbacd65f69333|1515327515000|1512543978000; aliyungf_tc=AQAAAEpMnz1D5QUAe9rWcetpEZ8e7W6v; _xsrf=c1e02c91-092d-47ba-901c-2e2f1b531180; __utmc=51854390; __utmv=51854390.100-1|2=registration_date=20150622=1^3=entry_date=20150622=1; l_cap_id="NDE2MjFmNTBkMGFlNGEzOGE5ZTMwMzZhODM4NjUyNWU=|1516693141|bbbf191ea8664198154fb787afd24237a013e6f5"; r_cap_id="MjU1M2IwYTk5NGMxNGI3MDg3YjhiMTc3NTkyMWFiYzg=|1516693141|d673cf2dcd9a4315cb08ae0b51707834dd51f115"; cap_id="NDUzNTkyNDA2NWU0NGIwNTkxN2ZhODdiYWNmNTY4ODk=|1516693141|e98bebc5f2cc0fe3f5936b75fe9507a9b3297cfb"; capsion_ticket="2|1:0|10:1516696678|14:capsion_ticket|44:NjdlNzg4ODEyYzVkNDk5ZmEwYWJhMzM5NGFkMGYyNmE=|ff5398c4457d21e87123e4b3d3cf699209ce9a4a03c38e28fbdc914eaaf4aa03"; z_c0="2|1:0|10:1516696680|4:z_c0|92:Mi4xeXhiTUFRQUFBQUFBUUlJd0tYN1hEQ1lBQUFCZ0FsVk5hRUpVV3dEMXRxd18tMWZSTVZSdGE2SFNFSC1HZU8tVnF3|3cfb689793e97fc51441f21d3c48c04ba619f57bc63f8c3091c004456638e3ed"; __utma=51854390.1338944023.1513399910.1516674947.1516696703.8; __utmb=51854390.0.10.1516696703; __utmz=51854390.1516696703.8.6.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
            'host': 'www.zhihu.com',
            'upgrade-insecure-requests': '1',
            'X-UDID': 'AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE='
        }
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        ]
        self.lock = lock
        self.ip = ip

    def get_headers(self, url_):
        user_agent = random.choice(self.ua_list)
        self.headers['Referer'] = url_
        self.headers['User-Agent'] = user_agent
        return self.headers

    def get_ajax(self, url, url_):
        try:
            response = session.get(url, headers=self.get_headers(url_), proxies=self.ip, timeout=5).content
            return json.loads(response)
        except Exception:
            print('网络连接错误！')
        # except requests.ConnectTimeout:
        #     print('代理ip延迟过高，请及时更换ip!')
        # except http.client.RemoteDisconnected:
        #     print('连接被中断！')

    def create_url(self, topic_id):
        url_ = 'https://www.zhihu.com/topic/{topic_id}/hot'.format(topic_id=topic_id)
        url_c = 'https://www.zhihu.com/api/v3/topics/{topic_id}/children'.format(topic_id=topic_id)
        url_p = 'https://www.zhihu.com/api/v3/topics/{topic_id}/parent'.format(topic_id=topic_id)
        url_data = 'https://www.zhihu.com/api/v4/topics/{topic_id}'.format(topic_id=topic_id)
        return url_, url_c, url_p, url_data

    def get_data(self, url_, url_c=None, url_p=None, url_data=None):
        if url_data:
            data = self.get_ajax(url_data, url_)
            return self.parse(data, 0)
        elif url_c:
            data = self.get_ajax(url_c, url_)
            return self.parse(data, 1)
        elif url_p:
            data = self.get_ajax(url_p, url_)
            return self.parse(data, 2)

    def parse(self, data, i):
        key_list = ['name', 'followers_count', 'questions_count', 'url', 'introduction']
        if i == 0:
            topic_dict = {}
            for key in key_list:
                topic_dict[key] = data[key]
            topic_dict['_id'] = data['id']
            return topic_dict
        else:
            data = data['data']
            relative_list = []
            for content in data:
                if i == 1:
                    if not self.save_db.find_one({'_id': content['id']}):
                        # print('该话题已存在！')
                        q.put(content['id'])
                relative_list.append(
                    {
                        'id': content['id'],
                        'name': content['name']
                    }
                )
            return relative_list

    def save_to_mongo(self, topic, children, parent):
        topic['children'] = children
        topic['parent'] = parent
        self.lock.acquire()
        try:
            if self.save_db.insert(topic):
                print('插入成功！')
        except errors.DuplicateKeyError:
            pass
        self.lock.release()

    def controll(self, topic_id):
        url_, url_c, url_p, url_data = self.create_url(topic_id)
        topic = self.get_data(url_, url_data=url_data)
        children = self.get_data(url_, url_c=url_c)
        parent = self.get_data(url_, url_p=url_p)
        self.save_to_mongo(topic, children, parent)


class ThreadCrawl(threading.Thread):
    def __init__(self, q, lock, ip=None):
        threading.Thread.__init__(self)
        self.q = q
        self.zhihu = ZhihuTopicTask(lock=lock, ip=ip)

    def run(self):
        topic_id = self.q.get()
        self.zhihu.controll(topic_id)


threads = []


def get_ip():
    ip_list = []
    for ip in db[MONGO_IP_TABLE].find():
        ip_list.append({'https': ip['https'],
                        'http': ip['https']
                        })
    return ip_list


def main():
    # ip_list = get_ip()
    # ip_list.append('')
    zhihu = ZhihuTopicTask(lock=lock)
    zhihu.controll('19776749')
    while not q.empty():
        sleep(3)
        for i in range(5):
            # ip = random.choice(ip_list)
            ip = None
            t = ThreadCrawl(q, lock, ip)
            t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
