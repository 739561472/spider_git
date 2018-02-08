import redis
from config import REDIS_HOST, REDIS_PORT


class RedisQueue(object):
    def __init__(self, name, namespace='queue'):
        self.__db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        self.key = ('%s:%s' % (namespace, name))

    def get_nowait(self):
        # 返回队列最右端元素，如果为空则返回空
        return self.__db.lpop(self.key)

    def url_sadd(self, url):
        # 将已经抓取的url加入到集合中
        return self.__db.sadd(self.key, url)

    def url_seens(self, url):
        # 判断url是否已经抓取
        return self.__db.sismember(self.key, url)

    def get_wait(self, timeout=None):
        # 返回队列最右端元素，如果为空则等待所有元素加入队列，至timeout
        return self.__db.blpop(self.key, timeout=timeout)

    def put(self, item):
        # 将元素加入队列最右端
        return self.__db.rpush(self.key, item)

    def count(self):
        # 返回队列中元素数量
        return self.__db.llen(self.key)

    def check(self, item):
        return self.__db.set(self.key, item)

