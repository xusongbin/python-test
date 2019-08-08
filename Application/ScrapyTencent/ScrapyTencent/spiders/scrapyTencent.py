# -*- coding: utf-8 -*-
import scrapy
from traceback import format_exc
from ScrapyTencent.items import ScrapytencentItem


class ScrapytencentSpider(scrapy.Spider):
    name = 'scrapyTencent'
    allowed_domains = ['tencent.com']
    url = 'https://careers.tencent.com/search.html?query=co_1&sc=1&index='
    offset = 1
    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for link in response.xpath('//div[@class="recruit-wrap recruit-margin"]/div'):
            try:
                item = ScrapytencentItem()
                item['title'] = link.xpath('a/h4/text()').extract()[0]
                item['part'] = link.xpath('a/p[1]/span[1]/text()').extract()[0]
                item['local'] = link.xpath('a/p[1]/span[2]/text()').extract()[0]
                item['type'] = link.xpath('a/p[1]/span[3]/text()').extract()[0]
                item['time'] = link.xpath('a/p[1]/span[4]/text()').extract()[0]
                # context = '{},{},{},{},{}\n'.format(
                #     item['title'], item['part'], item['local'], item['type'], item['time']
                # )
                # print(context)
                yield item
            except Exception as e:
                print('{}\n{}'.format(e, format_exc()))
        if self.offset < 2:
            self.offset += 1

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

