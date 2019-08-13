# -*- coding: utf-8 -*-
import re
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class QvodSpider(scrapy.Spider):
    name = 'qvod'
    allowed_domains = ['kuaibo-qvod.com']
    # start_urls = ['https://kuaibo-qvod.com/lipage/1.html']
    start_urls = []
    url = 'https://kuaibo-qvod.com/lipage/%d.html'
    for idx in range(1, 10):
        this_url = url % idx
        start_urls.append(this_url)

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        item = ScrapymmItem()
        if re.match(r'https://kuaibo-qvod\.com/lipage/\d+\.html', response.url):
            for a in response.xpath('//div[@class="index_pic gao"]/a'):
                next_url = self.base_url + a.xpath('@href').extract_first()
                if not next_url:
                    continue
                yield scrapy.Request(next_url, callback=self.parse)
        elif re.match(r'https://kuaibo-qvod\.com/qvod/\d+\.html', response.url):
            for a in response.xpath('//div[@class="img datu"]/a'):
                next_url = a.xpath('img/@src').extract_first()
                name = a.xpath('img/@data').extract_first()
                if not next_url:
                    continue
                if not name:
                    name = a.xpath('img/@alt').extract_first()
                    if not name:
                        print('QVOD NOT NAME: {}'.format(response.url))
                item['image_url'] = response.urljoin(next_url)
                item['image_name'] = handle_name(name)
                yield item
