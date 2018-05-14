# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

dic = {'news':'新闻','ent':'娱乐','sports':'体育','money':'财经','photo':'图片','auto':'汽车','idol':'星闻','war':'军事',
'video':'视频','liveshow':'直播','tech':'科技','mobile':'手机','digi':'数码','local':'本地','dy':'网易号','joke':'段子',
'lady':'时尚','tie':'跟帖','game':'游戏','edu':'教育','jiankang':'健康','exclusive':'独家','travel':'旅游','baby':'亲子',
'art':'艺术','shuangchuang':'双创','caipiao':'彩票'}

class NewsSpider(RedisSpider):
    name = 'newsspider'
    redis_key = 'newsspider:start_urls'
    start_urls = ['https://3g.163.com/']

    def start_requests(self):
        # reqs = [] 
        # base_url_front = 'https://3g.163.com/touch/'
        # base_url_end = '/?ver=c&clickfrom=index2018_header'
        # for key in dic:
        #     base_url = base_url_front + key + base_url_end
        #     yield scrapy.Request(url=base_url, callback=self.parse)
        base_url = 'https://3g.163.com/touch/news/?ver=c&clickfrom=index2018_header'
        yield scrapy.Request(url=base_url, callback=self.parse)
        
    def parse(self, response):
        print(response.text)
