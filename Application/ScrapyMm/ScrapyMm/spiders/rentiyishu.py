# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name
from urllib.parse import urljoin


class RentiyishuSpider(scrapy.Spider):
    name = 'rentiyishu'
    allowed_domains = ['rentiyishu.in']
    base_url = 'http://www.rentiyishu.in'
    start_urls = [
            'http://www.rentiyishu.in/zgrenti/',
            'http://www.rentiyishu.in/rbrenti/',
            'http://www.rentiyishu.in/omrenti/',
            'http://www.rentiyishu.in/ddrenti/',
            'http://www.rentiyishu.in/mnrenti/',
        ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        # print(url_this)
        # 照片链接
        next_url = response.xpath('//div[@id="bigpic"]/a/img/@src').extract_first()
        if next_url:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="con-5-l"]/span/text()').extract_first()
            item['image_url'] = response.urljoin(next_url).strip()
            item['image_name'] = handle_name(name)
            # print('{} {}'.format(item['image_name'], item['image_url']))
            yield item
        # 下一张照片
        next_url = response.xpath('//div[@class="page"]/ul/li/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 打开相册
        for li in response.xpath('//ul[@class="detail-list"]/li'):
            next_url = li.xpath('a/@href').extract_first()
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 获取下一页主题
        next_url = response.xpath('//div[@class="page-show"]/ul/li/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

