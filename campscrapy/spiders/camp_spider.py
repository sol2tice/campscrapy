import scrapy
from campscrapy.items import CampItem
from scrapy.http import Request
import urlparse

class CampSpider(scrapy.Spider):
    CONCURRENT_REQUESTS = 100
    LOG_LEVEL = 'INFO'
    COOKIES_ENABLED = False
    RETRY_ENABLED = False

    name = "camp"
    allowed_domains = ["meedow.com"]
    start_urls = [
	"http://www.meedow.com/program/"
    ]
    notfound = 0;

    def parse(self, response):
	for i in range(1, 1400): 
	  url = self.start_urls[0]+ str(i)
	  yield Request(url, callback = self.parse_program)
 	print 'Total notfound = %s' % self.notfound;

    def parse_program(self, response):
#        filename = response.url.split("/")[-2]
#        with open(filename, 'wb') as f:
#            f.write(response.body)
	if response.status == 404:
	  self.notfount += 1
	  print 'notfound = %s' % self.notfound
	  return

	item = CampItem()
	item['id'] = response.url[len('http://www.meedow.com/program/'):]
	print 'id = %s' % response.url[len('http://www.meedow.com/program/'):] 
	item['title'] = response.xpath('//div[@class="title"]/h2/text()').extract()[0]
	item['city'] = response.xpath('//div[@class="address"]/dd/text()').extract()[0]
	image_relative_url = response.xpath('//div[@class="picture large"]/img/@src').extract()[0]
	item['image_urls'] = [urlparse.urljoin(response.url, image_relative_url.strip())]
	sel = response.xpath('//div[@class="info-container"]')
	grad = ''
	for s in sel.xpath('//ul/li[1]//ul/li'):
	    grad = grad + s.xpath('text()').extract()[0] + ','
	
	item['grade'] = grad
	try:
          item['category'] = sel.xpath('//ul/li[2]/dd/text()').extract()[0]
	except IndexError:
	  pass
	try:
	  item['subject'] = sel.xpath('//ul/li[3]/dd/text()').extract()[0]
	except IndexError:
	  pass
	item['credit'] = sel.xpath('//ul/li[4]/dd/text()').extract()[0]
	item['type'] = sel.xpath('//ul/li[5]/dd/text()').extract()[0]
	item['price'] = sel.xpath('//ul/li[6]/dd/text()').extract()[0]
	try:
	  item['duration'] = sel.xpath('//ul/li[7]/dd/text()').extract()[0]
	except IndexError:
	  pass
	item['starton'] = sel.xpath('//ul/li[8]/dd/text()').extract()[0]
	item['deadline'] = sel.xpath('//ul/li[9]/dd/text()').extract()[0]
	sel = response.xpath('//div[@id="program-details"]')
	item['description'] = sel.xpath('section[@id="summary"]/p/text()').extract()[0]
	item['schoolinfo'] = sel.xpath('section[@id="school-info"]/p/text()').extract()[0]
	cost = sel.xpath('section[@id="time-cost"]/p/text()').extract()
	if len(cost) > 0:
	    item['timecost'] = cost[0]
	item['guide'] = sel.xpath('section[@id="apply-guide"]/p/text()').extract()[0]
	item['crimerate'] = sel.xpath('//div[@class="map-data-number"]/text()').extract()[0]
	item['weather'] = sel.xpath('//div[@class="map-data-number"]/a/text()').extract()[0]
	item['houseprice'] = sel.xpath('//div[@class="map-data-number"]/text()').extract()[2]
	item['asianpop'] = sel.xpath('//div[@class="map-data-number"]/text()').extract()[3]
	item['longitute'] = sel.xpath('//div[@id="myMap"]/@data-lng').extract()[0]
	item['latitute'] = sel.xpath('//div[@id="myMap"]/@data-lat').extract()[0]
        yield item
