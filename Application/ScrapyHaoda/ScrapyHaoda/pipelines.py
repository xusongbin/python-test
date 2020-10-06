# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os


class ScrapyhaodaPipeline:
    def __init__(self):
        self.filename = open("haoda2.csv", "a+", encoding='gbk')
        self.old = self.filename.read()

    def process_item(self, item, spider):
        _type = item['type']
        if _type == 'url':
            _page = item['page']
            _video = item['video']
            _name = item['name']
            _pic = item['pic']
            _data = '{},{},{},{}\n'.format(_page, _video, _name, _pic)
            _data = _data.encode().decode('gbk', 'ignore')
            if _video not in self.old:
                self.filename.write(_data)
        elif _type == 'img':
            _name = '{}.jpg'.format(item['name'])
            _img = item['img']
            with open(os.path.join('img', _name), 'wb') as f:
                f.write(_img)
        return item

    def close_spider(self, spider):
        self.filename.close()
