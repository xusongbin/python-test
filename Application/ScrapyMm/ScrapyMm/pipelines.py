# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import time
import shutil
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from ScrapyMm.settings import IMAGES_STORE
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['image_name'].strip():
            old_file = item['image_url'].replace('http://', '').replace('https://', '').replace('//', '/')
            old_file = IMAGES_STORE + '/' + old_file
            old_file = old_file.replace('\\', '/')
            file_name = os.path.basename(item['image_url'])
            new_file = item['image_name'].strip() + '/' + file_name
            new_file = IMAGES_STORE + '/' + new_file
            new_file = new_file.replace('\\', '/')
            if os.path.isfile(old_file):
                file_path = os.path.dirname(new_file)
                if not os.path.isdir(file_path):
                    os.mkdir(file_path)
                shutil.move(old_file, new_file)
                print('{} TO {}'.format(old_file, new_file))
            elif os.path.isfile(new_file):
                print('{} EXSIT'.format(new_file))
                pass
            else:
                print('{} DOWNLOAD'.format(new_file))
                yield scrapy.Request(item['image_url'], meta={'name': item['image_name']})

    def file_path(self, request, response=None, info=None):
        file_name = os.path.basename(str(request.url))
        new_path = request.meta['name'] + '/' + file_name
        return new_path
