# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem


class A45xmSpider(scrapy.Spider):
    name = '45xm'
    base_url = 'https://45xm.com'
    allowed_domains = ['45xm.com']
    start_urls = [
            'https://45xm.com/mnrt/',
            'https://45xm.com/rbrt/',
            'https://45xm.com/zgrt/'
        ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        # 获取下一页
        next_url = response.xpath('//div[@class="page-show"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 遍历当前网页的所有相册
        for li in response.xpath('//div[@class="wzlist"]/ul/li'):
            next_url = li.xpath('a/@href').extract_first()
            if next_url:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 当前相册下一张照片
        # next_url = response.xpath('//div[@class="pages"]/a[text()="下一页"]/@href').extract_first()
        # if next_url:
        #     yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 获取照片链接
        next_url = response.xpath('//div[@class="tu"]/a/img/@src').extract_first()
        if next_url:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="tu"]/a/img/@alt').extract_first()
            item['image_url'] = next_url
            item['image_name'] = name
            print('{} {}'.format(name, next_url))
            yield item

