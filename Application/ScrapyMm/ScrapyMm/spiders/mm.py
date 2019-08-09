# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem


class MmSpider(scrapy.Spider):
    name = 'mm'
    allowed_domains = ['mm131.one', 'tuigirls.net', 'tuigirls888.net', 'kuaibo-qvod.com', 'sinaimg.cn']
    # start_urls = ['https://mm131.one/mm/1_3.html']

    start_urls = []
    base_url = 'https://mm131.one/mm/%d.html'
    for idx in range(1, 2820):      # 2820
        now_url = base_url % idx
        start_urls.append(now_url)

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        now_url = response.url
        # print(response.text)
        next_url = None
        item = ScrapymmItem()
        for a in response.xpath('//div[@class="img gets"]/center/a'):
            try:
                src = a.xpath('img/@src').extract()[0]
                if src:
                    if 'http' not in src:
                        src = 'https://mm131.one' + src
                    if 'mm//mm' in src:
                        src = src.replace('mm//mm', 'mm')
                    item['image_url'] = src
                    yield item
            except:
                pass
            if next_url:
                continue
            try:
                href = a.xpath('@href').extract()[0]
                next_url = now_url[:now_url.rfind('/') + 1] + href
            except:
                pass
        if next_url:
            if 'mm//mm' in next_url:
                next_url = next_url.replace('mm//mm', 'mm')
            yield scrapy.Request(next_url, callback=self.parse)
