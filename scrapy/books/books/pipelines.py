# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BooksPipeline(object):
    def process_item(self, item, spider):
        return item
class PriceConventerPipeline():
    exchange_rate = 8.539
    def process_item(self, item, spider):
        #提取item的price字段
        #去掉前面的英镑符号，转换为string类型
        price = float(item['price']['1:'])*self.exchange_rate

        #将price保留两位小数并附回price字段
        item['price'] ='%.2f'%price


        return item