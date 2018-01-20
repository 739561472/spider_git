# coding:utf-8
import pymongo

from region.config import MONGO_DB, MONGO_TABLE
name = '阿坝州'
data = {'两年房价数据': [{'日期': '2017-01-23', '房价': 3212}, {'日期': '2017-01-30', '房价': 3235}]}

client = pymongo.MongoClient()
db = client[MONGO_DB]
db[MONGO_TABLE].update({'name': name}, {'$set': data})

