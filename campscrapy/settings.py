# -*- coding: utf-8 -*-

# Scrapy settings for campscrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'campscrapy'

SPIDER_MODULES = ['campscrapy.spiders']
NEWSPIDER_MODULE = 'campscrapy.spiders'
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en',
    'Referer': 'http://education-portal.com'
}
# 'Accept-Language': 'zh'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'campscrapy (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"

ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = './img'
IMAGES_EXPIRES = 90
IMAGES_THUMBS = {
    'small': (70, 40)
}
