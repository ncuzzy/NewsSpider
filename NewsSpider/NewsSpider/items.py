# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field() #娱乐
    digest = scrapy.Field() #简介
    title = scrapy.Field() #福原爱化身棒球少女
    time = scrapy.Field() #2018-05-13 23:39
    commentCount = scrapy.Field() #评论数
    source = scrapy.Field() #网易娱乐
    content = scrapy.Field() #正文
