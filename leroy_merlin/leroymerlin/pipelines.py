# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter





from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


import scrapy
from pymongo import MongoClient

#class DataBasePipeline:
#    def __init__(self):
#        self.client = MongoClient('localhost',27017)
#       self.mongo_base = self.client.leroy_photos
#   def process_item(self, item, spider):
#      collection = self.mongo_base[spider.name]
#        collection.insert_one(item)
#        return item
#    def __del__(self):
#        self.client.close()




class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img,meta=item)
                except Exception as e:
                    print(e)




    def file_path(self, request, response=None, info=None):
         item = request.meta
         href = str(item['url']).replace("https://kaliningrad.leroymerlin.ru/product/",'').replace("/", '')
         img_name = str(request.url).replace('https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_500,h_500,c_pad,b_white,d_photoiscoming.png/LMCode/', '')
         return f'/full/{href}/{img_name}'


    def item_completed(self, results, item, info):

       if results:
           item['photos'] = [itm[1] for itm in results if itm[0]]
       return item
    


