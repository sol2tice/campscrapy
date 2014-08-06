# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CampItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	id =scrapy.Field()
    	title = scrapy.Field()
	city = scrapy.Field()
    	grade = scrapy.Field()
   	category = scrapy.Field()
    	subject = scrapy.Field()
    	credit = scrapy.Field()
	type = scrapy.Field()
	price = scrapy.Field()
	duration = scrapy.Field()
	starton = scrapy.Field()
	deadline = scrapy.Field()
	description = scrapy.Field()
	schoolinfo = scrapy.Field()
	timecost = scrapy.Field()
	guide = scrapy.Field()
	crimerate = scrapy.Field()
	weather = scrapy.Field()
	houseprice = scrapy.Field()
	asianpop = scrapy.Field()
	longitute = scrapy.Field()
	latitute = scrapy.Field()
