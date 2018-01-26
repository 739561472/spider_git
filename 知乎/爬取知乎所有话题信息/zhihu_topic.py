# coding:utf-8
# import http.cookiejar
from http import cookiejar
import json
import random
import threading
from queue import Queue
from time import sleep
from pymongo import MongoClient, errors
import requests

from config import *
# from get_ip import *


q = Queue()
lock = threading.Lock()
client = MongoClient()
db = client[MONGO_DB]
session = requests.session()
# 读取之前存储的cookie文件



class ZhihuTopicTask:
    def __init__(self, lock, ip=None):
        self.save_db = db[MONGO_TOPIC_TABLE]# db[MONGO_TOPIC_TABLE]
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '_zap=0ad13437-1f6b-4d51-90e5-5fa9b3ee60ea; d_c0="AECCMCl-1wyPTj22u6rDh3P9kEgxFV88TZE=|1513399908"; q_c1=5ddb74d22f8249cf84ebbacd65f69333|1515327515000|1512543978000; aliyungf_tc=AQAAAEpMnz1D5QUAe9rWcetpEZ8e7W6v; _xsrf=c1e02c91-092d-47ba-901c-2e2f1b531180; anc_cap_id=379df63bac7247faa82fe82938e6263e; l_cap_id="NzdjYjNjMTY4MTgyNGQ0OThhZDc2MzYzNmE3ODA0MDE=|1516967370|01b788dec03a26c09486e3c408dde96415c22594"; r_cap_id="OTEzZTg5MTkyNDVhNGU5YWE1YmUzNDcxNGFhMzY2MDM=|1516967370|be6c4aa5b774d0b1fbe698b2bd569f51847785d8"; cap_id="YjJiMDQzNGIzMWZlNDk0Yzg0ZGExMmQyMDQxMjBlNDc=|1516967370|7b5c3e8a9d8b8de653e64eed5502f0f4650dbd94"; capsion_ticket="2|1:0|10:1516967377|14:capsion_ticket|44:NDM3N2YwYmM1NGU4NGQ4YTg4MTAyMDkzOWY5NjU5OWE=|41550cedbdf560b0dd703ec5a98b5d0bbd41200e291e71a4f7c37b1ea9c0c653"; z_c0="2|1:0|10:1516967379|4:z_c0|92:Mi4xeXhiTUFRQUFBQUFBUUlJd0tYN1hEQ1lBQUFCZ0FsVk4wMk5ZV3dCemhSUDFWb2FqNHpZVzRNYVNpY3VDaFBRMHZn|2c5dccf35c5ce6af733dfada1c305827279cbd112df7b13134f2549b9a16799c"; __utma=51854390.1427180410.1516967390.1516967390.1516967390.1; __utmb=51854390.0.10.1516967390; __utmc=51854390; __utmz=51854390.1516967390.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100-1|2=registration_date=20150622=1^3=entry_date=20150622=1',
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
        self.form_data = {'_xsrf': 'c1e02c91-092d-47ba-901c-2e2f1b531180'}
        self.url_, self.url_c, self.url_p, self.url_data = '', '', '', ''

    def get_headers(self, url_):
        # 定制请求头
        user_agent = random.choice(self.ua_list)
        self.headers['Referer'] = url_
        self.headers['User-Agent'] = user_agent
        return self.headers

    def get_ajax(self, url, url_, form_data=None):
        # 从接口获取ajax请求的数据，json.loads()解析
        try:
            if form_data:
                response = session.post(url, headers=self.get_headers(url_), data=form_data, proxies=self.ip,
                                        timeout=5).content
                print(response)
                return json.loads(response)
            else:
                response = session.get(url, headers=self.get_headers(url_), proxies=self.ip, timeout=5).content
                return json.loads(response)
        # 捕获Internet异常，这里是因为出现的异常有点多-_-||，精确捕获很麻烦，代码好像要很多，所以就偷懒--
        except Exception:
            print('网络连接错误！')
            # 若使用代理ip，出现异常后，更换ip，尝试再次获取数据
            if self.ip:
                self.exception_loop(url, form_data)

    def exception_loop(self, url, form_data):
        # 读取一个新的代理ip
        db[MONGO_IP_TABLE].delete_one({'https': self.ip['https']})
        self.ip = db[MONGO_IP_TABLE].find_one()
        self.get_ajax(url, self.url_, form_data)
        # except requests.ConnectTimeout:
        #     print('代理ip延迟过高，请及时更换ip!')
        # except http.client.RemoteDisconnected:
        #     print('连接被中断！')

    def create_url(self, topic_id):
        # 构造一个请求头使用的url和三个数据接口的url
        self.url_ = 'https://www.zhihu.com/topic/{topic_id}/hot'.format(topic_id=topic_id)
        self.url_c = 'https://www.zhihu.com/topic/{topic_id}/children'.format(topic_id=topic_id)
        self.url_p = 'https://www.zhihu.com/api/v3/topics/{topic_id}/parent'.format(topic_id=topic_id)
        self.url_data = 'https://www.zhihu.com/api/v4/topics/{topic_id}'.format(topic_id=topic_id)

    def get_data(self, url_, url_c=None, url_p=None, url_data=None):
        # 根据传入的url调用相应函数
        if url_data:
            data = self.get_ajax(url_data, url_)
            return self.parse(data, 0)
        elif url_c:
            data = self.get_ajax(url_c, url_, form_data=self.form_data)
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
                    data = self.get_ajax(url=data.get('paging').get('next'), url_=self.url_, form_data=self.form_data)
                    if isinstance(data, dict) and 'data' in data.keys():
                        c_data = c_data.join(data['data'])
                for content in c_data:
                    # 查重
                    if not self.save_db.find_one({'_id': content[0][2]}):
                        q.put(content[0][2])
                    relative_list.append(content[0][1])
                return relative_list

    def save_to_mongo(self, topic, children, parent):
        # 将传入的各个数据，整理，然后存储到数据库中
        topic['children'] = children
        topic['parent'] = parent
        # 这个时候，最好加锁，防止出现意外情况
        self.lock.acquire()
        try:
            if self.save_db.insert(topic):
                print('插入成功！')
        except errors.DuplicateKeyError:
            pass
        self.lock.release()

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
    session.cookies = cookiejar.LWPCookieJar(filename='cookie_zhihu')
    session.cookies.load(ignore_discard=True)
    # # test_ip()
    # # 设置第一项为空，可以默认为本机ip，毕竟本机ip才是最好的
    # ip_list = ['']
    # # 提取代理ip
    # for i in db[MONGO_IP_TABLE].find():
    #     ip_list.append(i)
    zhihu = ZhihuTopicTask(lock=lock)
    zhihu.controller('19776749')
    # 判断队列是否为空
    while not q.empty():
        sleep(3)  # 休眠时间，防止给服务器造成过大压力（其实是为了保护自己--）
        for i in range(6):
            # 随机取一个ip，也可以改成每隔多少次换一个ip
            # ip = random.choice(ip_list)
            ip = None
            # 加入线程
            t = ThreadCrawl(q, lock, ip)
            # 启动！
            t.start()
    for t in threads:
        # 阻塞线程，等待所有子线程结束后，在结束主线程
        t.join()


if __name__ == "__main__":
    main()
