import scrapy
import os.path
from time import gmtime, strftime

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    zhang_url = 'https://voice.baidu.com/Page/rank?query=zhangguorong'    

    def start_requests(self):                
        yield scrapy.Request(url=self.zhang_url, callback=self.record_number)

    def record_number(self, response):
        vote_zhang_tag = response.css("#viewport > div.common.target-star > span.target-star-vote > b").extract_first()        
        vote_zhang = vote_zhang_tag[3:-4]

        vote_gap_tag = response.css("#viewport > div.common.target-star > span.target-star-gap > b").extract_first()
        vote_gap = vote_gap_tag[3:-4]

        vote_wang = int(vote_gap.replace(',',''))+int(vote_zhang.replace(',',''))
        if os.path.exists("myfile.dat"):
            with open("myfile.dat", "a+") as fi:
                fi.write(str(vote_wang) +"\t"+vote_zhang+"\t"+ vote_gap+"\t" +strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"\n")
        else:
            with open("myfile.dat", "w") as fi:
                fi.write(str(vote_wang) + "\t"+vote_zhang+"\t"+ vote_gap+"\t" +strftime("%Y-%m-%d %H:%M:%S", gmtime()) +"\n")
