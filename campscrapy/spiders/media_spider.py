import scrapy
from campscrapy.items import Course, Chapter, VideoItem
from scrapy.http import Request
import urlparse
import re
import json
import time
import random

class MediaSpider(scrapy.Spider):
    CONCURRENT_REQUESTS = 1
    LOG_LEVEL = 'INFO'
    COOKIES_ENABLED = False
    RETRY_ENABLED = False

    name = "media"
    base_url = ''
    #allowed_domains = ["education-portal.com"]
    start_urls = ['http://wistia.com/']
    def __init__(self, media_file="../../courses/sat-math-2.json", domain="http://fast.wistia.com", url_prefix="http://fast.wistia.com/embed/medias/", *args, **kwargs):
        super(scrapy.Spider, self).__init__(*args, **kwargs)
        self.allowed_domains = [domain]
        self.base_url = domain
	self.url_prefix = url_prefix
        self.media_file = media_file

    def closed(self,reason):
	print json.dumps(self.courses)
	#super(MediaSpider, self).func()

    def parse(self, response):
	mf = open(self.media_file, "r")
        courses = json.load(mf)
	chapters = courses[0]['chapters']
	c = Course()
	self.courses = courses
	c['url'] = courses[0]['url']
	c['title'] = courses[0]['title']
	chapters2 = []
	c['chapters'] = chapters2
	for chapter in chapters:
	  ch = Chapter()
	  chapters2.append(ch)
	  ch['title'] = chapter['title']
	  ch['ch_num'] = chapter['ch_num']
	  lessons = chapter['lessons']
	  lessons2 = []
	  ch['lessons'] = lessons2
	  for lesson in lessons:
	    l = VideoItem()
	    lessons2.append(l)
	    l['title'] = lesson['title']
	    l['ch_num'] = lesson['ch_num']
	    l['l_num'] = lesson['l_num']
	    l['url'] = lesson['url']
	    l['hashcode'] = lesson['hashcode']
	    l['embed_url'] = lesson['embed_url']
	    time.sleep(int(random.uniform(1, 5)))
	    yield Request(self.url_prefix+l['hashcode']+'.json', meta={'item':l, 'lesson':lesson}, callback=self.parse_medias, dont_filter=True)
	#yield c

    def parse_medias(self, response):
	l = response.request.meta['item']
	lesson = response.request.meta['lesson']
	data = json.loads(response.body_as_unicode())
	l['mdmp4_url'] = data['media']['assets']['mdmp4']['url'].split('.bin')[0]
	lesson['mdmp4_url'] = l['mdmp4_url']
	yield Request(l['embed_url'], meta={'item':l, 'lesson':lesson}, callback=self.parse_media_object, dont_filter=True)

    def parse_media_object(self, response):
	l = response.request.meta['item']
	lesson = response.request.meta['lesson']
	data = json.loads(response.body_as_unicode())
	l['image_urls'] = [data['thumbnail_url']]
	lesson['image_urls'] = l['image_urls']
	yield l
