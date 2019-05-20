# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from pymongo import MongoClient
import os
import re

class Crawl1Pipeline(object):
    def open_spider(self, spider):
        if not os.path.exists("images"):
            os.mkdir("images")
        self.client = MongoClient()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item["title"] = re.sub('[\/:*?"<>| ]','-', item["title"])
        item["name"] = re.sub('[\/:*?"<>| ]','-', item["name"])
        item["image_name"] = re.sub('[\/:*?"<>| ]','-', item["image_name"])

        self.client["spider"]["mtl"].insert(dict(item))
        path = f"images/{item['title']}/{item['name']}"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/{item['image_name']}.jpg", "wb") as fp:
            fp.write(requests.get(item['image'], headers={"Referer": "https://www.meitulu.com"}).content)
            print(f"{path}/{item['image_name']}.jpg")

        return item
