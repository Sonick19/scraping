# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 12:51:20 2023

@author: Sofiia
"""
book={}
#get of pages in book
pages=int(input('pass number of pages:'))
#get books link from http://loveread.ec/
url= input('pass link to 1 page of book:')[:-1]
ind=url.rfind('=')
urls=[url+str(elem) for elem in range (1, pages+1)]
import scrapy

# Import the CrawlerProcess: for running the spider
from scrapy.crawler import CrawlerProcess

# Create the Spider class
class DC_Chapter_Spider(scrapy.Spider):
  name = "dc_chapter_spider"
  # start_requests method
  def start_requests(self):
      for url in urls:
          yield scrapy.Request(url = url,
                         callback = self.parse)
  # First parsing method
  def parse(self, response):
    text=response.css('p.MsoNormal ::text').extract()
    book[int(str(response)[ind+6:-1])]=text
            
# Run the Spider
process = CrawlerProcess()
process.crawl(DC_Chapter_Spider)
process.start()

with open('new50.txt', 'a', encoding='utf-8') as rt:
    for i in range(1, pages+1):
        for line in book[i]:
            rt.write(line)
