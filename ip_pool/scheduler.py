from time import sleep
from multiprocessing import Process
from proxytester import Tester
from config import *
from crawler import ProxyCrawler
from redis_db import RedisClient
from api import app


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = ProxyCrawler()

    def is_max(self):
        if self.redis.count() >= IP_MAX_COUNT:
            print(self.redis.count())
            print('IP池已达到数目上限')
            return True
        else:
            return False

    def run(self):
        if not self.is_max():
            # 遍历抓取函数，抓取ip
            for func in range(self.crawler.__CrawlFuncCount__):
                crawl_func = self.crawler.__CrawlFunc__[func]
                proxies = self.crawler.get_proxy(crawl_func)
                for proxy in proxies:
                    if self.redis.exists(proxy):
                        print('正在存储', proxy)
                        self.redis.add(proxy)


class Scheduler(object):

    def run_getter(self):
        getter = Getter()
        while True:
            getter.run()
            sleep(CHECK_CYCLE)

    def run_tester(self):
        tester = Tester()
        while True:
            tester.run()
            sleep(CHECK_CYCLE)

    def run_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        if TESTER:
            print('开始检测ip')
            tester_prosess = Process(target=self.run_tester)
            tester_prosess.start()
        if GETTER:
            print('开始抓取代理')
            getter_prosess = Process(target=self.run_getter)
            getter_prosess.start()
        if API:
            print('允许提取代理')
            api_prosess = Process(target=self.run_api)
            api_prosess.start()


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
