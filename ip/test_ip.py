# coding:utf-8
import socket
import urllib.request
import urllib.error
import pymongo
import threading

from config import *

client = pymongo.MongoClient()
db = client[MONGO_DB]
db_ip = db[MONGO_TABLE]

proxy_ip = []
id = []
queryArgs = {}
projectionFileds = {'ip': True, 'port': True,}
for item in db_ip.find(queryArgs, projection=projectionFileds):
    ip = {'HTTP'+'':''+item['ip']+':'+item['port']}
    proxy_ip.append(ip)
    id.append(item['_id'])
lock = threading.Lock()
def test(i):
    socket.setdefaulttimeout(5)
    url = 'https://www.lagou.com/jobs/list_'
    try:
        #print(proxy_ip[i])
        proxy_handler = urllib.request.ProxyHandler(proxy_ip[i])
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        res = urllib.request.urlopen(url).read()
        lock.acquire()
        print(i,'号ip可以使用',id[i])
        lock.release()
    except urllib.error.HTTPError as e:
        lock.acquire()
        print(i,'号ip不可以使用')
        db_ip.remove({'_id': id[i]})
        lock.release()
test(1)
threads = []
for i in range(len(proxy_ip)):
    thread = threading.Thread(target=test,args=[i])
    threads.append(thread)
    thread.start()
# 阻塞主进程，等待所有子进程结束
for thread in threads:
    thread.join()


