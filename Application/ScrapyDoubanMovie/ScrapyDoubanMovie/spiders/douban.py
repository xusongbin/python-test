# -*- coding: utf-8 -*-
import scrapy
from ScrapyDoubanMovie.items import ScrapydoubanmovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/27010768/comments?status=P']

    def parse(self, response):
        assert isinstance(response, scrapy.http.Response)
        print(response.url)
        for usr in response.xpath('//div[@id="comments"]/div[@class="comment-item"]'):
            try:
                item = ScrapydoubanmovieItem()
                item['movie'] = response.xpath('//div[@id="content"]/h1/text()').extract_first()
                item['user'] = usr.xpath('div[@class="avatar"]/a/@title').extract_first()
                item['cid'] = usr.xpath('@data-cid').extract_first()
                item['rating'] = usr.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@title').extract_first()
                item['votes'] = usr.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span[1]/text()').extract_first()
                item['time'] = usr.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[3]/@title').extract_first()
                item['context'] = usr.xpath('div[@class="comment"]/p/span/text()').extract_first()
                # print('{} {} {}'.format(item['movie'], item['user'], item['cid']))
                # print('{} {} {}'.format(item['rating'], item['votes'], item['time']))
                # print('{}'.format(item['context']))
                yield item
            except Exception as e:
                print(e)
        next_page = response.xpath('//div[@id="paginator"]/a[@class="next"]/@href').extract_first()
        if next_page:
            url_this = response.url
            url_head = url_this[: url_this.rfind('?')]
            url_next = url_head + next_page
            yield scrapy.Request(url_next, callback=self.parse)
