# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydoubanmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie = scrapy.Field()
    user = scrapy.Field()
    cid = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()
    time = scrapy.Field()
    context = scrapy.Field()
