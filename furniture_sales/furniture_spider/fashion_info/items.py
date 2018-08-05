# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FashionInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fname = scrapy.Field()
    content = scrapy.Field()
    price = scrapy.Field()
    img = scrapy.Field()
    sales = scrapy.Field()
    url = scrapy.Field()
