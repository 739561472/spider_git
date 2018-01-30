# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BossjobPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    db_connection = 'boss_job'

    def __init__(self, mongo_uri, mongo_db):
        self.mong_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=(crawler.settings.get('MONGO_URI')),
            mongo_db=(crawler.settings.get('MONGO_DB'))
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.db_connection].update({'_id': item['_id']}, {'$set': dict(item)}, True)
        return item
