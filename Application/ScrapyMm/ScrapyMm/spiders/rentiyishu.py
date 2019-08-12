# -*- coding: utf-8 -*-
import scrapy


class RentiyishuSpider(scrapy.Spider):
    name = 'rentiyishu'
    allowed_domains = ['rentiyishu.in']
    start_urls = [
            'http://www.rentiyishu.in/zgrenti/',
            'http://www.rentiyishu.in/rbrenti/',
            'http://www.rentiyishu.in/omrenti/',
            'http://www.rentiyishu.in/ddrenti/',
            'http://www.rentiyishu.in/mnrenti/',
        ]

    def parse(self, response):
        pass
