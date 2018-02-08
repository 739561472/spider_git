# encoding: utf-8
import pymongo
from config import MONGO_DB, MONGO_TABLE
from redis_db import RedisQueue


class Pipelines(object):
    def __init__(self):
        self.__db = RedisQueue('save')
        item = self.__db.get_wait()


class MongoPipelines(Pipelines):
    def __init__(self):
        super(Pipelines).__init__()
        self.client = pymongo.MongoClient()
        self.mongodb = self.client[MONGO_DB]


