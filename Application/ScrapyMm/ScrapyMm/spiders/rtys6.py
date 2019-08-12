# -*- coding: utf-8 -*-
import scrapy


class Rtys6Spider(scrapy.Spider):
    name = 'rtys6'
    allowed_domains = ['rtys6.com']
    start_urls = [
            'http://rtys6.com/ArtZG/',
            # 'http://rtys6.com/ArtOM/',
            # 'http://rtys6.com/ArtRB/',
            # 'http://rtys6.com/ArtDD/',
            # 'http://rtys6.com/ArtZXY/',
            # 'http://rtys6.com/ArtMET/'
        ]

    def parse(self, response):
        print(response.text)
        # img = response.xpath('//div[@class="imgbox"]/a/img/@src').extract_first()
        # print(img)
        # if img:
        #     name = response.xpath('/h1/a/text()').extract_first()
        #     print('{} {}'.format(name, img))
        # this_url = response.url
        # head_url = 'http://rtys6.com'
        # next_href = response.xpath('//div[@class="pagelist"]/a[text()="下一页"]/@href').extract_first()
        # if next_href:
        #     next_url = this_url[: this_url.rfind('/')+1] + next_href
        #     yield scrapy.Request(next_url, callback=self.parse)
        # for li in response.xpath('//div[@class="fzltp"]/ul/li'):
        #     next_href = li.xpath('a/@href').extract_first()
        #     if next_href:
        #         next_url = head_url + next_href
        #         yield scrapy.Request(next_url, callback=self.parse)
