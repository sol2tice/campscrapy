import scrapy
from campscrapy.items import Course, Chapter, VideoItem
from scrapy.http import Request
import urlparse
import re
import time
import random

class CourseSpider(scrapy.Spider):
    CONCURRENT_REQUESTS = 1
    LOG_LEVEL = 'INFO'
    COOKIES_ENABLED = False
    RETRY_ENABLED = False

    name = "chapter"
    base_url = 'http://education-portal.com'
    #allowed_domains = ["education-portal.com"]
    start_urls = ["http://education-portal.com/academy/course/gre-test.html"]

    def parse(self, response):
        c = Course()
        c['url'] = response.url
        print 'url = '+ c['url']
        c['title'] = response.xpath('//h1/text()').extract()[0]

        chapter_paths = response.xpath('//div[@class="programCourse noBorder"]')
        chapters = []
        c['chapters'] = chapters
	for i, chapter in enumerate(chapter_paths):
	  ch = Chapter()
	  ch['title'] = chapter.xpath('h2/a/text()').extract()[0]
	  ch['ch_num'] = i+1
	  chapters.append(ch)
	  lesson_paths = chapter.xpath('div[@class="chapterList"]/ul/li')
	  lessons =[]
	  ch['lessons'] = lessons
	  for j, l in enumerate(lesson_paths):
	    l_url = l.xpath('a/@href').extract()[0]
	    ll = VideoItem()
	    ll['ch_num'] = i+1
	    ll['l_num'] = j+1
	    lessons.append(ll)
	    time.sleep(int(random.uniform(1, 20)))
	    yield Request(self.base_url+l_url, meta={'item':ll}, callback=self.parse_lesson)
  	yield c

    def parse_lesson(self, response):
	print 'the url = '+response.url
	#item = VideoItem()
	item = response.meta['item']
        item['url'] = response.url
	item['title'] = response.xpath('//title/text()').extract()[0]
        sel = response.xpath('//div[starts-with(@id, "wistia_")]')
	item['hashcode'] = sel.xpath('@id').extract()[0].split('_')[1]
	item['embed_url'] = 'http://fast.wistia.com/oembed.json?url=http://home.wistia.com/medias/' + item['hashcode'] + '?embedType=seo&maxwidth=600px&maxheight=330px'	
	yield item
