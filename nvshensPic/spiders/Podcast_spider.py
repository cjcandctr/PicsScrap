
import scrapy
import os
from pathlib import Path
import json
import time

class PodcastSpider(scrapy.Spider):
    name = "dsSpider"
    #baseUrl = "http://www.dataskeptic.com/podcast?limit=10&offset=0"  
    baseUrl = "http://www.dataskeptic.com/api/v1/podcasts?limit=15&offset=0&firstLoad=true"
    folder = "./output/"

    def start_requests(self):
        yield scrapy.Request(url=self.baseUrl, callback=self.build_album_base)

    def build_album_base(self, response):
        if(not os.path.exists(self.folder)):
            os.makedirs(self.folder)
        resJson = json.loads(response.body_as_unicode())
        if "items" in resJson:
            for item in resJson["items"]:
                for related in item["related"]:
                    if related["type"] == "mp3":
                        name = related["dest"].split('/')[-1]
                        name = name[0:name.find("?")]
                        desc_file = Path(self.folder + name)
                        if not desc_file.is_file():
                            yield scrapy.Request(url=related["dest"], callback=self.save_to_disk)
                        else:
                            self.logger.info('downloaded, skip...')
    def save_to_disk(self, response):
        name = response.url.split('/')[-1]
        name = name[0:name.find("?")]
        desc_file = Path(self.folder + name)
        if not desc_file.is_file():
            self.logger.info('Saving audio %s', self.folder + name)
            with open(self.folder + name, 'wb') as f:
                f.write(response.body)
        
    # def get_page_image(self, response):
    #     desc = response.css("#htilte::text").extract()[0] + ".txt"
    #     for imgTag in response.css("#hgallery img::attr(src)"):            
    #         yield scrapy.Request(url = imgTag.extract(), callback=self.save_image, meta={"desc":desc})

    # def save_image(self, response):
    #     start = response.url.find("gallery")+8
    #     end = start + [m.start() for m in re.finditer('/', response.url[start:])][1]
    #     folder = "./output/" + response.url[start:end] + "/"
    #     if(not os.path.exists(folder)):
    #         os.makedirs(folder)
        
    #     desc_file = Path(folder+ response.meta["desc"])
    #     if not desc_file.is_file():
    #         open(folder+response.meta["desc"], 'a').close()
    #     filename = folder + response.url[[m.start() for m in re.finditer('/', response.url)][-1]+1:]
    #     with open(filename, 'wb') as pic_f:
    #         pic_f.write(response.body)
    #     self.log('Saved file %s' % filename)
