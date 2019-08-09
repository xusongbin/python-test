# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time


class ScrapyimagePipeline(object):

    def process_item(self, item, spider):
        save_url = item['name']
        save_path, save_name = os.path.split(save_url)
        cur_path = ''
        for name in save_path.split('/'):
            cur_path += '{}/'.format(name)
            if not os.path.isdir(cur_path):
                os.mkdir(cur_path)
        if not os.path.isfile(save_url):
            with open(save_url, 'wb') as f:
                f.write(item['data'])
            print('{:.3f}: {}'.format(time.time(), save_url))
        return item
