import scrapy
from campscrapy.items import Course, Chapter, VideoItem
from scrapy.http import Request
import urlparse
import re

class CourseSpider(scrapy.Spider):
    CONCURRENT_REQUESTS = 2
    LOG_LEVEL = 'INFO'
    COOKIES_ENABLED = False
    RETRY_ENABLED = False

    name = "course"
    base_url = ''
    #allowed_domains = ["education-portal.com"]
    start_urls = []

    def __init__(self, course_file="course_file", domain="http://education-portal.com", url_prefix="http://education-portal.com/academy/course/", *args, **kwargs):
	super(scrapy.Spider, self).__init__(*args, **kwargs)
	self.allowed_domains = [domain]
	self.base_url = domain
	cf = open(course_file, "r")
        urls = cf.read().split(',')
	for i in urls:
	  course = re.sub(r'\s+', ' ', i, flags=re.UNICODE)
	  course = course.strip(' \n')
          self.start_urls.append(url_prefix+course+'.html')

    def parse(self, response):
	c = Course()
        c['url'] = response.url
	print 'url = '+ c['url']
	c['title'] = response.xpath('//h1/text()').extract()[0]
	
	chapter_paths = response.xpath('//div[@class="programCourse noBorder"]')
	chapters = []
	for i, chapter in enumerate(chapter_paths):
	  ch = Chapter()
	  ch['title'] = chapter.xpath('h2/a/text()').extract()[0]
	  ch['seq_num'] = i+1
	  chapters.append(ch)
	  lessons = []
	  lesson_paths = chapter.xpath('div[@class="chapterList"]/ul/li')
	  for lesson in lesson_paths:
	    l = VideoItem()
	    #l['title'] = lesson.xpath('a/@title').extract()[0]
	    lesson_url = lesson.xpath('a/@href').extract()[0]
	    id = lesson.xpath('a/span/text()').extract()[0]
	    l['seq_num'] = id[0:len(id)-1]
	    l['url'] = self.base_url+lesson_url
	    lessons.append(l)
	    yield Request(self.base_url+lesson_url, meta={'item':l}, callback=self.parse_lesson)
	  ch['lessons'] = lessons
	  yield ch
	c['chapters'] = chapters		  
	yield c

    def parse_lesson(self, response):
	print 'url = '+response.url
	#item = VideoItem()
	item = VideoItem(response.meta['item'])
	#item['seq_num'] = response.meta['id']
        item['url'] = response.url
	item['title'] = response.xpath('//title/text()').extract()[0]
        sel = response.xpath('//div[starts-with(@id, "wistia_")]')
	item['hashcode'] = sel.xpath('@id').extract()[0].split('_')[1]
	item['embed_url'] = 'http://fast.wistia.com/oembed.json?url=http://home.wistia.com/medias/' + item['hashcode'] + '?embedType=seo&maxwidth=600px&maxheight=330px'	
	yield item
