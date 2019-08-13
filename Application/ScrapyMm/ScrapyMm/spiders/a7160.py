# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class A7160Spider(scrapy.Spider):
    name = '7160'
    allowed_domains = ['7160.com']
    start_urls = [
        'https://www.7160.com/rentiyishu',
        'https://www.7160.com/xiaohua/',
        'https://www.7160.com/weimeitupian/',
        'https://www.7160.com/meinvmingxing/',
        'https://www.7160.com/qingchunmeinv/',
    ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        img = response.xpath('//div[@class="picsbox picsboxcenter"]/p/a/img/@src').extract_first()
        if img:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="picsbox picsboxcenter"]/p/a/img/@alt').extract_first()
            item['image_url'] = img
            item['image_name'] = handle_name(name)
            yield item
        for row in response.xpath('//div[@class="news_bom-left"]/div[@class="new-img"]'):
            for col in row.xpath('ul/li'):
                url_href = col.xpath('a/@href').extract_first()
                if not url_href:
                    continue
                yield scrapy.Request(response.urljoin(url_href), callback=self.parse)
        page_next = response.xpath(
            '//div[@class="page"]/a[text()="下一页"]/@href|'
            '//div[@class="itempage"]/a[text()="下一页"]/@href'
        ).extract_first()
        if page_next:
            yield scrapy.Request(response.urljoin(page_next), callback=self.parse)
