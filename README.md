campscrapy
==========
http://doc.scrapy.org/en/latest/intro/tutorial.html
scrapy shell 'http://www.meedow.com/program/364'
To config languate setting, in ~/campscrapy/campscrapy/settings.py add
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en',
}
# 'Accept-Language': 'zh'
$ cd ~/campscrapy/
$ scrapy crawl camp -o camdata.json 2>err 1>out
