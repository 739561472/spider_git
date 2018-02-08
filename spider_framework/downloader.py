# encoding: utf-8
from urllib.parse import urljoin
import hashlib
import asyncio
import aiohttp
import pickle
import random
from config import *
from redis_db import RedisQueue


def is_redirect(status_code):
    return status_code in (301, 302, 300, 307, 303)


class Spider(object):
    def __init__(self, _args):
        self.db = RedisQueue('work')
        self.ua = DEFLAUT_UA
        self.headers = {}
        self.timeout = TIMEOUT
        self.delay_time = DELAY_TIME
        self.proxy_ip = None
        self.max_redirect = MAX_REDIRECT
        self._seen = RedisQueue('urlseen')
        self._args = pickle.loads(_args)

    def url_add(self, url):
        # 摘要算法
        md5 = hashlib.md5()
        md5.update(url.encode('utf-8'))
        return md5.hexdigest()

    def allow_args(self):
        url = self._args.get('url')
        self.headers = self._args.get('headers') if self._args.get('headers') else self.headers
        ip = self._args.get('ip') if PROXY_IP == 1 else None
        self.timeout = self._args.get('timeout') if PROXY_IP == 1 else TIMEOUT
        if not self.headers:
            self.headers['User_Agent'] = random.choice(self.ua)
        if not url.startswith('http' or 'https'):
            raise ValueError('url必须以http或https开头')
        if self._seen.url_seens(self.url_add(url)):
            pass
        if ip:
            self.proxy_ip = {
                'http': 'http://%s' % ip,
            }
        return url

    async def fetch(self):
        url = self.allow_args() if self.allow_args() else print('url已经抓取拉')
        post_data = self._args.get('post_data')
        if not post_data:
            try:
                print(url)
                self._seen.url_sadd(self.url_add(url))
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url, headers=self.headers, proxy=self.proxy_ip,
                                           timeout=self.timeout) as response:
                        if self.check_code(response.status):
                            return await response.text()
                        else:
                            self.redirect(response, url)
                            # 重定向问题待处理
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(e, "网络连接错误！！")
        elif post_data:
            if isinstance(post_data, dict):
                self._seen.url_sadd(self.url_add(url))
                async with aiohttp.ClientSession() as session:
                    async with session.post(url=url, headers=self.headers, data=post_data, proxy=self.proxy_ip,
                                            timeout=self.timeout) as response:
                        if self.check_code(response.status):
                            return await response.text()
                        else:
                            self.redirect(response, url)
                        # 重定向问题待处理
            else:
                raise TypeError('post_data必须是字典形式')
        else:
            raise ValueError('method类型错误')

    def check_code(self, status_code):
        if status_code == 200:
            return True
        elif is_redirect(status_code):
            return False

    def redirect(self, response, url):
        location = response.headers['location']
        next_url = urljoin(url, location)
        if self._seen.url_seens(self.url_add(url)):
            return
        else:
            self.db.put(next_url)







