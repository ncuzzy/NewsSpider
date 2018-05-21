# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from NewsSpider.items import NewsspiderItem
import pymongo
import settings

class NewsspiderPipeline(object):
    def __init__(self):
        # 连接复制集
        self.client = pymongo.MongoClient('107.172.188.221:27017', replicaset='my_repl')
        # 获得数据库
        self.db = self.client['News']  
        # 获得集合
        self.coll = self.db['WangYiNews']  

    def process_item(self, item, spider):
        if (isinstance(item, NewsspiderItem)):
            self.coll.insert(dict(item))
        return item
