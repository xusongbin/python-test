# -*- coding: utf-8 -*-
import re
import os
import scrapy
from ScrapyHaoda.items import ScrapyhaodaItem


class ScrapyimgSpider(scrapy.Spider):
    name = 'getImg'
    allowed_domains = []
    start_urls = []
    name_dict = {}
    old_list = os.listdir('img')
    with open('haoda2.csv', 'r') as f:
        while True:
            link = f.readline()
            if not link:
                break
            if not re.match(r'.*,.*,.*,http.*', link):
                continue
            _name = link.split(',')[2]
            link = link.split(',')[3].strip()
            if not re.match(r'http.*\.jpg', link):
                continue
            if _name not in old_list:
                name_dict[link] = _name
                start_urls.append(link)
    # print(start_urls)

    def parse(self, response):
        if response.url in self.name_dict.keys():
            item = ScrapyhaodaItem()
            item['type'] = 'img'
            item['name'] = self.name_dict[response.url]
            item['img'] = response.body
            print(item['name'])
            yield item
