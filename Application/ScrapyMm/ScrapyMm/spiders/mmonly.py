# -*- coding: utf-8 -*-
import re
import scrapy
from ScrapyMm.items import ScrapymmItem


class MmonlySpider(scrapy.Spider):
    name = 'mmonly'
    allowed_domains = ['mmonly.cc']
    start_urls = ['http://www.mmonly.cc/mmtp/']

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        item = ScrapymmItem()
        # 查找提交主题的照片
        img = response.xpath('//div[@id="big-pic"]/p/a/img/@src').extract_first()
        if img:
            name = response.xpath('//div[@id="big-pic"]/p/a/img/@alt').extract_first().strip()
            if not name:
                print('MMONLY NOT NAME: {}'.format(response.url))
            item['image_url'] = img
            item['image_name'] = name
            # print('{} {}'.format(alt, img))
            yield item
        # 查找主题下一张图片
        next_url = response.xpath('//div[@class="pages"]/ul/li[@id="nl"]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 查找主题的链接
        for a in response.xpath('//div[@class="ABox"]/a'):
            href = a.xpath('@href').extract_first()
            if not href:
                continue
            yield scrapy.Request(href, callback=self.parse)
        # 查找主题下一页
        next_url = response.xpath('//div[@id="pageNum"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
