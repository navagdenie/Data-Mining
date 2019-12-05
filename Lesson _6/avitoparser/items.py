# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def cleaner_string(value):
    return value.replace('\n ', '').replace('\xa0', ' ')

class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    house_square = scrapy.Field(input_processor=MapCompose(cleaner_string))
    land_square = scrapy.Field()
    material = scrapy.Field()
    stairs = scrapy.Field()
    address = scrapy.Field(input_processor=MapCompose(cleaner_string))
    price = scrapy.Field(output_processor=TakeFirst())

