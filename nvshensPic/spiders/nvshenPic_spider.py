import scrapy
import os
from pathlib import Path
import re

class NvshensPicSpider(scrapy.Spider):
    name = "nvshensPic"
    baseUrl = "https://www.nvshens.com/gallery/heisi/"    
    pager_urls = []    
    album_urls = []
    def start_requests(self):                
        yield scrapy.Request(url=self.baseUrl, callback=self.build_album_base)

    def build_album_base(self, response):
        for atag in response.css("a.galleryli_link::attr(href)"):
            if atag.extract() not in self.album_urls:
                self.album_urls.append(atag.extract())
        for link in self.album_urls:            
            yield scrapy.Request(url=response.urljoin(link), callback=self.build_pager)            

    def build_pager(self, response):
        pager = response.css("div#pages")[0]
        for link in pager.css("a::attr(href)").extract():
            if link not in self.pager_urls:                    
                self.pager_urls.append(link)
        last2 = self.pager_urls[-2]
        for page in self.pager_urls:            
            next_page = response.urljoin(page)
            yield scrapy.Request(url=next_page, callback = self.get_page_image)
        
    def get_page_image(self, response):
        desc = response.css("#htilte::text").extract()[0] + ".txt"
        for imgTag in response.css("#hgallery img::attr(src)"):            
            yield scrapy.Request(url = imgTag.extract(), callback=self.save_image, meta={"desc":desc})

    def save_image(self, response):
        start = response.url.find("gallery")+8
        end = start + [m.start() for m in re.finditer('/', response.url[start:])][1]
        folder = "./output/" + response.url[start:end] + "/"
        if(not os.path.exists(folder)):
            os.makedirs(folder)
        
        desc_file = Path(folder+ response.meta["desc"])
        if not desc_file.is_file():
            open(folder+response.meta["desc"], 'a').close()
        filename = folder + response.url[[m.start() for m in re.finditer('/', response.url)][-1]+1:]
        with open(filename, 'wb') as pic_f:
            pic_f.write(response.body)
        self.log('Saved file %s' % filename)
