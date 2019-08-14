# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class Mm131Spider(scrapy.Spider):
    name = 'mm131'
    allowed_domains = ['mm131.one']
    base_url = 'https://mm131.one'
    # start_urls = ['https://mm131.one/mm/1.html']

    start_urls = []
    for idx in range(1, 2820):
        url_this = base_url + '/mm/{}.html'.format(idx)
        start_urls.append(url_this)

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        # 获取当前照片链接
        img = response.xpath('//div[@class="img gets"]/center/a/img/@src').extract_first()
        if img:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="title jgfgh"]/h1/text()').extract_first()
            item['image_url'] = response.urljoin(img)
            item['image_name'] = handle_name(name)
            yield item
        # 获取下一张照片连接
        next_img = response.xpath('//div[@class="pagebread"]/li/a[text()="下一页"]/@href').extract_first()
        if next_img:
            yield scrapy.Request(response.urljoin(next_img), callback=self.parse)
