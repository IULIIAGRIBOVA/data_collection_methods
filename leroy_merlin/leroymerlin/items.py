# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(value):
    if value!=None:
        value = value.replace('w_82', 'w_500')
        value = value.replace('h_82', 'h_500')
    if value[:2] == '//':
        return f'http:{value}'
    else:
        return value

def str_to_int(value):
    return int(value[0].replace(' ', ''))

class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:

    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor= str_to_int, output_processor=TakeFirst())
    def_list = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())




