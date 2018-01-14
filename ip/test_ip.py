# coding:utf-8
import pymongo
import threading
import requests

from config import *

client = pymongo.MongoClient()
db = client[MONGO_DB]
db_ip = db[MONGO_TABLE]

proxy_ip = []
ip_id = []
queryArgs = {}
projectionFileds = {'ip': True}
for item in db_ip.find(queryArgs, projection=projectionFileds):
    ip = {'HTTP': item['ip']}
    proxy_ip.append(ip)
    ip_id.append(item['_id'])
lock = threading.Lock()


def test(i):
    headsers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    # url = 'http://ip.chinaz.com/getip.aspx'
    # url = 'https://www.zhihu.com/'
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    try:
        res = requests.get(url, headsers, proxies=proxy_ip[i], timeout=3)
        if res:
            print(i, '号ip可以使用', proxy_ip[i])
        else:
            lock.acquire()
            print(i, '号ip不可以使用')
            db_ip.remove({'_id': ip_id[i]})
            lock.release()
    except requests.ConnectTimeout:
        lock.acquire()
        print(i, '号ip不可以使用')
        db_ip.remove({'_id': ip_id[i]})
        lock.release()


test(1)

threads = []
for i in range(len(proxy_ip)):
    thread = threading.Thread(target=test, args=[i])
    threads.append(thread)
    thread.start()
# 阻塞主进程，等待所有子进程结束
for thread in threads:
    thread.join()


