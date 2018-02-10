# coding:utf-8
# from http import cookiejar
import json
import random
import threading
from queue import Queue
from time import sleep
from pymongo import MongoClient, errors
import requests

from config import *


q = Queue()
lock = threading.Lock()
client = MongoClient()
db = client[MONGO_DB]
session = requests.session()


class ZhihuTopicTask:
    def __init__(self, lock, ip=None):
        self.save_db = db[MONGO_TOPIC_TABLE]# db[MONGO_TOPIC_TABLE]
        self.headers = {
            'accept': 'accept:application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_zap=0ad13437-1f6b-4d51-90e5-5fa9b3ee60ea; d_c0="AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE=|1513399908"; q_c1=5ddb74d22f8249cf84ebbacd65f69333|1515327515000|1512543978000; aliyungf_tc=AQAAAEpMnz1D5QUAe9rWcetpEZ8e7W6v; _xsrf=c1e02c91-092d-47ba-901c-2e2f1b531180; anc_cap_id=379df63bac7247faa82fe82938e6263e; __utmc=51854390; __utmv=51854390.100-1|2=registration_date=20150622=1^3=entry_date=20150622=1; l_cap_id="MzVlMmYwNzcyYTAwNDgyNTliYmZiY2U0OTEwYmM4NDA=|1516968241|98d6e55c113ee21bcc58946f42ad250ac7869461"; r_cap_id="MDFmNmYzMmQ1OTkwNGU5NTkzYzc1ZTVkMjBiYTQ2N2E=|1516968241|29f41ee1c2e1a76221403ee64fd1c7ab46eff2b3"; cap_id="YjY0NmJjMTQ4NmI4NDg3MDg0NzkwZjNmNTIyZTdiODQ=|1516968241|8251cb78de27be99fd237373f43d79e3bab28d21"; capsion_ticket="2|1:0|10:1516970322|14:capsion_ticket|44:ODQ0YWMzYTJlMjQzNDI5Mzk3YzFmOWZlMDYyMzI2ZDM=|61d103d1483ab7edb7b56f32063e9e2fe5ca08dce2352d020d1ae36cbcc08289"; __utma=51854390.1427180410.1516967390.1516967390.1516971796.2; __utmb=51854390.0.10.1516971796; __utmz=51854390.1516971796.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
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
        self.url_, self.url_c, self.url_p, self.url_data = '', '', '', ''

    def get_headers(self, url_):
        # 定制请求头
        user_agent = random.choice(self.ua_list)
        self.headers['Referer'] = url_
        self.headers['User-Agent'] = user_agent
        return self.headers

    def get_ajax(self, url, url_):
        # 从接口获取ajax请求的数据，json.loads()解析
        try:
            response = session.get(url, headers=self.get_headers(url_), proxies=self.ip, timeout=5).text
            return json.loads(response)
        # 捕获Internet异常，这里出现的异常有点多-_-||
        except requests.HTTPError as e:
            print(e)
        except ConnectionResetError as e:
            print(e)
            # # 若使用代理ip，出现异常后，更换ip，尝试再次获取数据
            # if self.ip:
            self.exception_loop(url)

    def exception_loop(self, url):
        # 读取一个新的代理ip
        # db[MONGO_IP_TABLE].delete_one({'https': self.ip['https']})
        # self.ip = db[MONGO_IP_TABLE].find_one()
        self.get_ajax(url, self.url_)
        # except requests.ConnectTimeout:
        #     print('代理ip延迟过高，请及时更换ip!')
        # except http.client.RemoteDisconnected:
        #     print('连接被中断！')

    def create_url(self, topic_id):
        # 构造一个请求头使用的url和三个数据接口的url
        self.url_ = 'https://www.zhihu.com/topic/{topic_id}/hot'.format(topic_id=topic_id)
        self.url_c = 'https://www.zhihu.com/api/v3/topics/{topic_id}/children'.format(topic_id=topic_id)
        self.url_p = 'https://www.zhihu.com/api/v3/topics/{topic_id}/parent'.format(topic_id=topic_id)
        self.url_data = 'https://www.zhihu.com/api/v4/topics/{topic_id}?include=introduction%2Cquestions_count%2Cbest_answers_count%2Cfollowers_count%2Cis_following'.format(topic_id=topic_id)

    def get_data(self, url_, url_c=None, url_p=None, url_data=None):
        # 根据传入的url调用相应函数
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
        # 进行数据筛选
        # 设置需要的key
        key_list = ['name', 'followers_count', 'questions_count', 'url', 'introduction']
        # 根据i判断传入的数据种类
        if i == 0:
            topic_dict = {}
            # 判断数据是否为字典形式，是否存在需要的key，防止出现Keyerror
            if isinstance(data, dict) and 'id' in data.keys():
                for key in key_list:
                    topic_dict[key] = data[key]
                topic_dict['_id'] = data['id']
                return topic_dict
        elif i == 2:
            if isinstance(data, dict) and 'data' in data.keys():
                data = data['data']
                relative_list = []
                for content in data:
                    relative_list.append(content['name'])
                    # 检查数据库中是否有已存在该数据，如不存在，将id放入队列
                    if not self.save_db.find_one({'_id': content['id']}):
                        q.put(content['id'])
                return relative_list
        else:
            relative_list = []
            if isinstance(data, dict)and'data'in data.keys():
                c_data = data['data']
                # 判断数据是否加载完毕
                while data.get('paging').get('is_end') is False:
                    # 提取下一页url
                    data = self.get_ajax(url=data.get('paging').get('next'), url_=self.url_)
                    print(data.get('paging').get('next'))
                    if isinstance(data, dict) and 'data' in data.keys():
                        c_data = c_data+data['data']
                for content in c_data:
                    # 查重
                    if not self.save_db.find_one({'_id': content['id']}):
                        q.put(content['id'])
                    relative_list.append(content['name'])
                return relative_list

    def save_to_mongo(self, topic, children, parent):
        # 将传入的各个数据，整理，然后存储到数据库中
        topic['children'] = children
        topic['parent'] = parent
        try:
            if self.save_db.insert(topic):
                print('插入成功！')
        except errors.DuplicateKeyError:
            pass

    def controller(self, topic_id):
        # 制定函数执行流程
        self.create_url(topic_id)
        topic = self.get_data(self.url_, url_data=self.url_data)
        children = self.get_data(self.url_, url_c=self.url_c)
        parent = self.get_data(self.url_, url_p=self.url_p)
        if topic is not None:
            self.save_to_mongo(topic, children, parent)


class ThreadCrawl(threading.Thread):
    # 开启多线程
    def __init__(self, q, lock, ip=None):
        threading.Thread.__init__(self)
        self.q = q
        self.zhihu = ZhihuTopicTask(lock=lock, ip=ip)

    def run(self):
        topic_id = self.q.get()
        self.zhihu.controller(topic_id)


threads = []


def main():
    # # 设置第一项为空，可以默认为本机ip，毕竟本机ip是最快的
    # ip_list = ['']
    # # 提取代理ip
    # for i in db[MONGO_IP_TABLE].find():
    #     ip_list.append(i)
    if db[MONGO_BK_TABLE].find():
        for token in db[MONGO_BK_TABLE].find():
            q.put(token['token'])
        db[MONGO_BK_TABLE].remove({})
    else:
        zhihu = ZhihuTopicTask(lock=lock)
        zhihu.controller('19776751')  # 选择开始爬取话题
    # 判断队列是否为空
    while not q.empty():
        sleep(1)  # 休眠时间，防止给服务器造成过大压力（其实是为了保护自己--）
        for i in range(6):
            # 随机取一个ip，也可以改成每隔多少次换一个ip
            # ip = random.choice(ip_list)
            t = ThreadCrawl(q, lock, ip=None)  # 加入线程
            t.start()
    for t in threads:
        # 阻塞主线程，等待所有子线程结束后，结束主线程
        t.join()


if __name__ == '__main__':
    main()
