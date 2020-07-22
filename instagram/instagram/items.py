# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_id = scrapy.Field()
    photo = scrapy.Field()
    follower = scrapy.Field()
    full_name_follower =  scrapy.Field()
    isfollower =scrapy.Field()


