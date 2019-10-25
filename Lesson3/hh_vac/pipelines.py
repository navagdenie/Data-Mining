# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class HhVacPipeline(object):
    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        db = client.hh
        self.collection = db.hh_vac

    def process_item(self, item, spider):
        self.collection.insert_one(item)
        return item
