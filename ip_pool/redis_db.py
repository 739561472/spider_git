import re
import redis
from config import *
from random import choice
from error import EmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=PROXY_SATUS_INIT):
        if not re.match(r'\d+\.\d+\.\d+.\d+\:\d+', proxy):
            # 不符合的代理丢弃
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        # 随机取出一个代理ip，默认从分数大到小
        result = self.db.zrangebyscore(REDIS_KEY, PROXY_SCORE_MAX, PROXY_SCORE_MIN)
        if result:
           return choice(result)
        else:
           result = self.db.zrevrange(REDIS_KEY, 0, 100)
           if result:
                return choice(result)
           else:
               raise EmptyError

    def remove(self, proxy):

        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > 19:
            # 代理ip分数减一
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            # 移除代理ip
            print('代理', proxy, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        # 判断ip是否存在
        return not self.db.zscore(REDIS_KEY, proxy)

    def max(self, proxy):
        # 将ip的分数置为max
        return self.db.zadd(REDIS_KEY, PROXY_SCORE_MAX, proxy)

    def count(self):
        # 返回代理ip总数
        return self.db.zcard(REDIS_KEY)

    def all(self):
        return

    def batch(self, start, stop):
        # 批量获取代理
        return self.db.zrange(REDIS_KEY, start, stop-1)



