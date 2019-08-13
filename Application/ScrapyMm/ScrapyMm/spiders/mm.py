# -*- coding: utf-8 -*-
import re
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


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
        next_url = None
        item = ScrapymmItem()
        for a in response.xpath('//div[@class="img gets"]/center/a'):
            try:
                src = a.xpath('img/@src').extract_first()
                if not src:
                    continue
                name = a.xpath('img/@alt').extract_first().strip()
                if not name:
                    name = response.xpath('//h1/text()').extract_first().strip()
                    if not name:
                        print('MM NOT NAME: {}'.format(response.url))
                item['image_url'] = response.urljoin(src)
                item['image_name'] = handle_name(name)
                yield item
            except:
                pass
            if next_url:
                continue
            try:
                href = a.xpath('@href').extract_first()
                if href:
                    next_url = response.urljoin(href)
            except:
                pass
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
