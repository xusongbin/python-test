# -*- coding: utf-8 -*-
import re
import scrapy
from ScrapyImage.items import ScrapyimageItem


class ScrapyimgSpider(scrapy.Spider):
    name = 'scrapyImg'
    allowed_domains = ['www.rentiyishu.in']
    link_file = 'src_rentiyishu.csv'
    start_urls = []
    with open(link_file, 'r') as f:
        while True:
            link = f.readline()
            if not link:
                break
            link = link.strip()
            if not re.match(r'http.*\.jpg', link):
                continue
            start_urls.append(link)

    def parse(self, response):
        item = ScrapyimageItem()
        item['name'] = response.url.replace('http://', '').replace('https://', '')
        item['data'] = response.body
        print(item['name'])
        yield item
