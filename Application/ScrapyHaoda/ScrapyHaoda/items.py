# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyhaodaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()
    page = scrapy.Field()
    video = scrapy.Field()
    name = scrapy.Field()
    pic = scrapy.Field()
    img = scrapy.Field()
    pass
