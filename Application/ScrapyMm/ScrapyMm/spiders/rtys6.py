# -*- coding: utf-8 -*-
import scrapy
from ScrapyMm.items import ScrapymmItem
from ScrapyMm.spiders.HandleName import handle_name


class Rtys6Spider(scrapy.Spider):
    name = 'rtys6'
    base_url = 'https://rtys6.com'
    allowed_domains = ['rtys6.com']
    start_urls = [
            'http://rtys6.com/ArtZG/',
            'http://rtys6.com/ArtOM/',
            'http://rtys6.com/ArtRB/',
            'http://rtys6.com/ArtDD/',
            'http://rtys6.com/ArtZXY/',
            'http://rtys6.com/ArtMET/'
        ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        # 获取图片链接
        next_url = response.xpath('//div[@class="imgbox"]/a/img/@src').extract_first()
        if next_url:
            item = ScrapymmItem()
            name = response.xpath('//div[@class="contitle"]/span/h1/a/text()').extract_first()
            item['image_url'] = next_url
            item['image_name'] = handle_name(name)
        # 已打开相册链接，该相册有几张图片，打开下一张图片的连接
        next_url = response.xpath('//div[@class="page"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 已打开主题列表，枚举每个主题跳转到主题的连接
        for li in response.xpath('//div[@class="fzltp"]/ul/li'):
            next_url = li.xpath('a/@href').extract_first()
            if not next_url:
                continue
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
        # 已打开主页链接，获取到主题列表一共N页，当前跳转到下一页。
        # 已打开主题链接，该主题下的相册列表有很多页，获取下一页链接
        next_url = response.xpath('//div[@class="pagelist"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
