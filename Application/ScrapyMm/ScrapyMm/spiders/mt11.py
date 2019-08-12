# -*- coding: utf-8 -*-
import re
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class Mt11Spider(scrapy.Spider):
    name = 'mt11'
    allowed_domains = ['mt11.xyz']
    # start_urls = ['http://mt11.xyz/tlist_31_0.html']

    start_urls = []
    base_url = 'http://mt11.xyz/tlist_31_%d.html'
    for idx in range(7):
        next_url = base_url % idx
        start_urls.append(next_url)

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        item = ScrapymmItem()
        if 'var imgs = [' in response.text:
            text = response.text
            img = text[text.find('var imgs') + 12:]
            img = img[:img.find(']')]
            name = response.xpath('//div[@class="tuku"]/div[@class="title"]/text()').extract_first()

            for im in re.findall(r'http.*\.jpg', img):
                item['image_url'] = im
                item['image_name'] = handle_name(name)
                yield item
        for a in response.xpath('//div[@class="container"]/article/a[@class="tuItem"]'):
            href = a.xpath('@href').extract_first()
            if not href:
                continue
            url = 'http://mt11.xyz/' + href
            yield scrapy.Request(url, callback=self.parse)
