import scrapy
import os
import csv
from pathlib import Path
import re

class ApeSpider(scrapy.Spider):
    custom_settings = {
        "DOWNLOAD_DELAY": 1.4,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 25
    }
    name = "Ape51"
    baseUrl = "http://www.51ape.com/zhuanji/index.html"    
    pager_urls = []    
    album_urls = {}
    def start_requests(self):                
        yield scrapy.Request(url=self.baseUrl, callback=self.build_album_base)
        base_addr = 'http://www.51ape.com/zhuanji/index_'
        for i in range(2,49):
            addr=base_addr + str(i)+".html"
            yield scrapy.Request(url=addr, callback=self.build_album_base)
        self.write_to_file()

    def build_album_base(self, response):
        for liTag in response.css("body > div.bg_wh.all.m > div > div.fl.over.w638 > div.fl.over.w638.mt_2 > div.news.over.fl > ul > li"):
            addr = liTag.css("a::attr(href)").extract()[0]
            yield scrapy.Request(url=addr, callback=self.parse_detail_page)    
         
    def parse_detail_page(self, response):
        title = response.css("body > div.bg_wh.all.m > div > div.fl.over.w638 > a::attr(title)").extract()[0]
        bd_addr = response.css("body > div.bg_wh.all.m > div > div.fl.over.w638 > a::attr(href)").extract()[0]
        access_tag = response.css("body > div.bg_wh.all.m > div > div.fl.over.w638 > b").extract()[0]
        access_code = access_tag[-8:-4]
        self.album_urls[len(self.album_urls)]=(title, bd_addr, access_code)

 
    def write_to_file(self):
        folder = "./output/"
        if(not os.path.exists(folder)):
            os.makedirs(folder)
        filename = folder + 'address.csv'
        writter = csv.writer(open(filename, "w"))
        self.log('Saved file %s' % filename)
        for key, val in self.album_urls.items():
            self.log('Current index: ' + str(key))
            writter.writerow([key, val])
