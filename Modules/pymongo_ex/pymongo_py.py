#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo


class MyMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017/')
        # print(self.client.list_database_names())
        self.db = self.client['runoobdb']
        self.col = self.db['sites']
        self.col1 = self.db['sites1']

        # self.insert_dict()
        # self.insert_list()
        # self.insert_with_id()
        # self.find_one()
        # self.find_all()
        # self.find_item({'name': 'QQ'})  # 按字段内容查询
        # self.find_item({'name': {'$gt': 'H'}})  # 查询第一个字母 ASCII 值大于 "H" 的数据
        # self.find_item({'name': {'$regex': '^R'}})  # 正则查找第一个字母为 "R" 的数据
        # self.find_to_dict({"_id": 0, "name": 1, "alexa": 1, "address": 1})    # 要显示的列集合
        # self.find_limit(3)

        # self.update_one({'alexa': '1000'}, {'$set': {'alexa': '12345'}})
        # self.update_one({'alexa': {'$regex': r'^1\d+5$'}}, {'$set': {'alexa': '12346'}})

        # self.find_sort('alexa', -1)

        # self.delete_one({'name': 'Taobao'})
        # self.delete_many({'alexa': {'$regex': r'^10\d$'}})
        # self.delete_many({})    # 传入空集合删除所有
        self.delete_drop()      # 删除一个集合

    def insert_dict(self):
        mydict = {'name': 'RB', 'alexa': '1000', 'url': 'https://www.runoob.com'}
        x = self.col.insert_one(mydict)
        print(x.inserted_id)

    def insert_list(self):
        mylist = [
            {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
            {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
            {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
            {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
            {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
        ]
        x = self.col.insert_many(mylist)
        print(x.inserted_ids)

    def insert_with_id(self):
        mylist = [
            {"_id": 1, "name": "RUNOOB", "cn_name": "菜鸟教程"},
            {"_id": 2, "name": "Google", "address": "Google 搜索"},
            {"_id": 3, "name": "Facebook", "address": "脸书"},
            {"_id": 4, "name": "Taobao", "address": "淘宝"},
            {"_id": 5, "name": "Zhihu", "address": "知乎"}
        ]
        x = self.col1.insert_many(mylist)
        print(x.inserted_ids)

    def find_one(self):
        x = self.col.find_one()
        print(x)

    def find_all(self):
        for x in self.col.find():
            print(x)

    def find_item(self, rule):
        for x in self.col.find(rule):
            print(x)

    def find_to_dict(self, rule):
        for x in self.col.find({}, rule):
            print(x)

    def find_limit(self, num):
        for x in self.col.find().limit(num):
            print(x)

    def update_one(self, query, new):
        self.col.update_one(query, new)
        for x in self.col.find():
            print(x)

    def find_sort(self, title, method=1):
        # method (1, -1)
        for x in self.col.find().sort(title, method):
            print(x)

    def delete_one(self, rule):
        self.col.delete_one(rule)
        for x in self.col.find():
            print(x)

    def delete_many(self, rule):
        x = self.col.delete_many(rule)
        print(x.deleted_count)
        for x in self.col.find():
            print(x)

    def delete_drop(self):
        self.col.drop()


if __name__ == '__main__':
    mm = MyMongo()
