# -*- coding: utf-8 -*-
import scrapy


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['mm131.one']
    start_urls = ['http://mm131.one/']

    def parse(self, response):
        pass
