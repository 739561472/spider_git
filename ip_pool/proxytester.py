from redis_db import RedisClient, TEST_COUNT_
from config import CHECK_URL
import asyncio
import aiohttp
import sys


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_proxy(self, proxy):
        # 使用异步测试代理ip可用性
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                proxy_t = 'http://' + proxy
                async with session.get(CHECK_URL, proxy=proxy_t, timeout=5, allow_redirects=False) as response:
                    if response.status == 200:
                        print('代理可用：', proxy)
                        self.redis.max(proxy)
                    else:
                        print('代理请求失败', proxy)
            except (
                    aiohttp.ClientError, aiohttp.client_exceptions.ClientConnectorError,
                    asyncio.TimeoutError, AttributeError, TypeError
                    ):
                self.redis.remove(proxy)

    def run(self):
        count = self.redis.count()
        try:
            # 分批测试代理ip可用性
            for n in range(0, count, TEST_COUNT_):
                start = n
                stop = min(n + TEST_COUNT_, count)
                proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                task = [self.test_proxy(proxy) for proxy in proxies]
                loop.run_until_complete(asyncio.gather(*task))
                sys.stdout.flush()
        except ValueError as e:
            print('发生', e, '异常')





