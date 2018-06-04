# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from NewsSpider.settings import MongoDB_URL,MongoDB_DBName,MongoDB_CollectionName,MongoDB_ReplSetName
from NewsSpider.items import NewsspiderItem
import pymongo
import settings

class NewsspiderPipeline(object):
    def __init__(self):
        # 连接复制集
        self.client = pymongo.MongoClient(MongoDB_URL), replicaset=MongoDB_ReplSetName)
        self.client = pymongo.MongoClient(MongoDB_URL) #, replicaset=MongoDB_ReplSetName
        # 获得数据库
        self.db = self.client[MongoDB_DBName]  
        # 获得集合
        self.coll = self.db[MongoDB_CollectionName]  

    def process_item(self, item, spider):
        if (isinstance(item, NewsspiderItem)):
            self.coll.insert(dict(item))
        return item
