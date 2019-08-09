# -*- coding: utf-8 -*-
import re
import os
import scrapy
from ScrapyImage.items import ScrapyimageItem


class ScrapyimgSpider(scrapy.Spider):
    name = 'scrapyImg'
    allowed_domains = []
    start_urls = []
    with open('src_rtys6.csv', 'r') as f:
        while True:
            link = f.readline()
            if not link:
                break
            link = link.strip()
            if not re.match(r'http.*\.jpg', link):
                continue
            save_path = link.replace('http://', '').replace('https://', '')
            if os.path.isfile(save_path):
                continue
            start_urls.append(link)
    with open('src_rentiyishu.csv', 'r') as f:
        while True:
            link = f.readline()
            if not link:
                break
            link = link.strip()
            if not re.match(r'http.*\.jpg', link):
                continue
            save_path = link.replace('http://', '').replace('https://', '')
            if os.path.isfile(save_path):
                continue
            start_urls.append(link)

    def parse(self, response):
        item = ScrapyimageItem()
        item['name'] = response.url.replace('http://', '').replace('https://', '')
        item['data'] = response.body
        # print(item['name'])
        yield item
