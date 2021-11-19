# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeroyparserPipeline:

    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.leroy_db = client["products"]

    def process_item(self, item, spider):
        collection = self.leroy_db[spider.name]
        collection.insert_one(item)
        return item


class ProductImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        photos = item["photos"]
        if photos:
            for img in photos:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item["photos"] = [itm[1] for itm in itm if itm[0]]
        return item