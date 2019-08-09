# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_url'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        # assert isinstance(request, scrapy.Request)
        cur_url = str(request.url)
        save_path = cur_url.replace('http://', '').replace('https://', '').replace('//', '/')
        # save_dir = os.path.dirname(save_path)
        # now_dir = ''
        # for name in save_dir.split('/'):
        #     now_dir += '{}/'.format(name)
        #     if not os.path.isdir(now_dir):
        #         os.mkdir(now_dir)
        return save_path
