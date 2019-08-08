# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapytencentPipeline(object):
    def __init__(self):
        self.file = open('record.csv', 'w')

    def process_item(self, item, spider):
        context = '{},{},{},{},{}\n'.format(
            item['title'], item['part'], item['local'], item['type'], item['time']
        )
        self.file.write(context.encode('bgk').decode('utf-8'))
        return item

    def close_spider(self, spider):
        self.file.close()
