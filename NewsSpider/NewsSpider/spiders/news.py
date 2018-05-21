# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider 
from NewsSpider.items import NewsspiderItem

chn_dic = {'news':'新闻','ent':'娱乐','sports':'体育','money':'财经','photo':'图片','auto':'汽车','idol':'星闻','war':'军事',
'video':'视频','liveshow':'直播','tech':'科技','mobile':'手机','digi':'数码','local':'本地','dy':'网易号','joke':'段子',
'lady':'时尚','tie':'跟帖','game':'游戏','edu':'教育','jiankang':'健康','exclusive':'独家','travel':'旅游','baby':'亲子',
'art':'艺术','shuangchuang':'双创','caipiao':'彩票'}
url_dic = {'news':'https://3g.163.com/touch/reconstruct/article/list/BBM54PGAwangning/*-20.html',
'ent':'https://3g.163.com/touch/reconstruct/article/list/BA10TA81wangning/*-20.html',
'sports':'https://3g.163.com/touch/reconstruct/article/list/BA8E6OEOwangning/*-20.html',
'money':'https://3g.163.com/touch/reconstruct/article/list/BA8EE5GMwangning/*-20.html',
'photo':'https://3g.163.com/photocenter/api/list/0001/00AN0001,00AO0001/*/20/cache_00AN_00AO_.json',
'auto':'https://3g.163.com/touch/reconstruct/article/list/BA8DOPCSwangning/*-20.html',
'idol':'https://star.3g.163.com/star/hot/articles/*-20.html?callback=getHotList',
'war':'https://3g.163.com/touch/reconstruct/article/list/BAI67OGGwangning/*-20.html',
'video':'https://3g.163.com/touch/nc/api/video/recommend/Video_Recom/*-20.do?callback=getVideoList',
#'liveshow':'直播',
'tech':'https://3g.163.com/touch/reconstruct/article/list/BA8D4A3Rwangning/*-20.html',
'mobile':'https://3g.163.com/touch/reconstruct/article/list/BAI6I0O5wangning/*-20.html',
'digi':'https://3g.163.com/touch/reconstruct/article/list/BAI6JOD9wangning/*-20.html',
#'local':'本地',
'dy':'https://3g.163.com/touch/reconstruct/article/list/BBM50AKDwangning/*-20.html',
'joke':'https://3g.163.com/touch/jsonp/joke/chanListNews/T1419316284722/2/*-20.html?callback=joke1',
'lady':'https://3g.163.com/touch/reconstruct/article/list/BA8F6ICNwangning/*-20.html',
'tie':'https://3g.163.com/touch/jsonp/hot/comments/*-20.html',
'game':'https://3g.163.com/touch/reconstruct/article/list/BAI6RHDKwangning/*-20.html',
'edu':'https://3g.163.com/touch/reconstruct/article/list/BA8FF5PRwangning/10-10*-20.html',
'jiankang':'https://3g.163.com/touch/reconstruct/article/list/BDC4QSV3wangning/*-20.html',
'exclusive':'https://3g.163.com/touch/reconstruct/article/list/BAI5E21Owangning/*-20.html',
'travel':'https://3g.163.com/touch/reconstruct/article/list/BEO4GINLwangning/*-20.html',
'baby':'https://3g.163.com/touch/reconstruct/article/list/BEO4PONRwangning/*-20.html',
'art':'https://3g.163.com/touch/reconstruct/article/list/CKKS0BOEwangning/*-20.html',
'shuangchuang':'https://3g.163.com/touch/reconstruct/article/list/CQU85FTDlizhenzhen/*-20.html',
'caipiao':'https://3g.163.com/touch/reconstruct/article/list/BVATQC54wangning/*-20.html'}

class NewsSpider(RedisSpider):
    name = 'newsspider'
    redis_key = 'newsspider:start_urls'
    start_urls = ['https://3g.163.com/']

    def start_requests(self):
        step = "10"
        for key in url_dic:
            for i in range (0,300,20):
                url_raw = url_dic[key]
                url_base = url_raw.replace("*",str(i))
                yield scrapy.Request(url=url_base, callback=self.parse)
        
    def parse(self, response):
        json_raw = response.text[9:-1]
        json_dic = json.loads(json_raw)
        for key in json_dic.keys():
            for i in range (0,20):
                newsUrl = json_dic[key][i]["url"]
                if(re.match(r"http://3g.163.com",newsUrl)):
                    item = NewsspiderItem()
                    item['digest'] = json_dic[key][i]["digest"] #str
                    item['title'] = json_dic[key][i]["title"] #str
                    item['time'] = json_dic[key][i]["ptime"] #str
                    item['commentCount'] = json_dic[key][i]["commentCount"] #int
                    item['source'] = json_dic[key][i]["source"] #str
                    yield Request(newsUrl, callback = self.parse_content, meta={'item':item})
                    
    def parse_content(self, response):
        item = response.meta['item']
        keyWord = re.match(r'http://.*?/(.*?)/', response.url).group(1)
        if keyWord in chn_dic:
            item['category'] = chn_dic[keyWord] #str
        else:
            item['category'] = "未知" #str
        raw_content = response.xpath("//div[@class='content']//p").extract()
        if(len(raw_content) > 0):
            content = "".join(raw_content)
            item['content'] = content
            yield item