# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class InstagramPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.insta

    def process_item(self, item, spider):
        if item['isfollower'] == True:
            collection = self.mongo_base['followers']
            collection.insert_one(item)
        else:
            collection = self.mongo_base['following']
            collection.insert_one(item)
        return item

    def __del__(self):
        self.client.close()


