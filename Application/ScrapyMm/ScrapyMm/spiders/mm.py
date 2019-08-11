# -*- coding: utf-8 -*-
import re
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
                src = a.xpath('img/@src').extract_first()
                if src:
                    if 'http' not in src:
                        src = 'https://mm131.one' + src
                    if 'mm//mm' in src:
                        src = src.replace('mm//mm', 'mm')
                    name = a.xpath('img/@alt').extract_first().strip()
                    if not name:
                        name = response.xpath('//h1/text()').extract_first().strip()
                        if not name:
                            print('MM NOT NAME: {}'.format(response.url))
                    name = re.sub(r'[？\\*|“<>:/]', '', name)
                    name = name.replace('标题：', '')
                    if re.match(r'.*\((\d+|图\d+)\)', name):
                        name = name[:name.find('(')]
                    if re.match(r'【.*】.*', name):
                        name = name[name.rfind('】')+1:]
                    if re.match(r'\[.*\].*', name):
                        name = name[name.rfind(']')+1:]
                    if re.match(r'.* \d+', name):
                        name = name[: name.rfind(' ')]
                    item['image_url'] = src
                    item['image_name'] = name
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
