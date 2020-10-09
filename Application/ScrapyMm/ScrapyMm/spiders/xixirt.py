# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem


class RentiyishuSpider(scrapy.Spider):
    name = 'xixirt'
    allowed_domains = ['xixirt.org']
    base_url = 'http://xixirt.org'
    start_urls = [
            'https://xixirt.org/ribenrentiyishu/',
            'https://xixirt.org/rentiyishusheying/',
            'https://xixirt.org/xixirentiyishu/',
            'https://xixirt.org/dadanrentiyishu/'
        ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        # 获取主题下一页
        next_url = response.xpath('//div[@class="page-show"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 遍历相册下一个主题
        for li in response.xpath('//ul[@class="detail-list"]/li'):
            next_url = li.xpath('a/@href').extract_first()
            if next_url:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 获取相册下一页
        # next_url = response.xpath('//div[@class="page-show"]/a[text()="下一页"]/@href').extract_first()
        # if next_url:
        #     yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 获取照片链接
        next_url = response.xpath('//div[@class="pp hh"]/a/img/@src').extract_first()
        if next_url:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="pp hh"]/a/img/@alt').extract_first()
            item['image_url'] = response.urljoin(next_url).strip()
            item['image_name'] = name
            print('{} {}'.format(item['image_name'], item['image_url']))
            yield item

