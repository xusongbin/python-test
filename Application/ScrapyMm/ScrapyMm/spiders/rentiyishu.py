# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class RentiyishuSpider(scrapy.Spider):
    name = 'rentiyishu'
    allowed_domains = ['rentiyishu.in']
    base_url = 'http://www.rentiyishu.in'
    start_urls = [
            'http://www.rentiyishu.in/zgrenti/',
            # 'http://www.rentiyishu.in/rbrenti/',
            # 'http://www.rentiyishu.in/omrenti/',
            # 'http://www.rentiyishu.in/ddrenti/',
            # 'http://www.rentiyishu.in/mnrenti/',
        ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        url_this = response.url
        url_head = url_this[: url_this.rfind('/') + 1]
        # print(url_this)
        # 照片链接
        img = response.xpath('//div[@id="bigpic"]/a/img/@src').extract_first()
        if img:
            item = ScrapymmItem()
            img = self.base_url + img
            name = response.xpath('//div[@class="con-5-l"]/span/text()').extract_first()
            item['image_url'] = img
            item['image_name'] = handle_name(name)
            yield item
        # 下一张照片
        page_next = response.xpath('//div[@class="page"]/ul/li/a[text()="下一页"]/@href').extract_first()
        if page_next:
            if 'html' in page_next:
                url_next = url_head + page_next
            else:
                url_next = self.base_url + page_next
            yield scrapy.Request(url_next, callback=self.parse)
        # 打开相册
        for li in response.xpath('//ul[@class="detail-list"]/li'):
            page_next = li.xpath('a/@href').extract_first()
            url_next = self.base_url + page_next
            yield scrapy.Request(url_next, callback=self.parse)
        # 获取下一页主题
        page_next = response.xpath('//div[@class="page-show"]/ul/li/a[text()="下一页"]/@href').extract_first()
        if page_next:
            if 'html' in page_next:
                url_next = url_head + page_next
            else:
                url_next = self.base_url + page_next
            yield scrapy.Request(url_next, callback=self.parse)

