# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GdsqItem(scrapy.Item):
    station = scrapy.Field()
    time = scrapy.Field()
    water_level = scrapy.Field()
    flow = scrapy.Field()
    warning_water_level = scrapy.Field()


class GdwaterItem(scrapy.Item):
    thread = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    site = scrapy.Field()
    time = scrapy.Field()
    water_level = scrapy.Field()
    warning_level = scrapy.Field()
    water_potemtial = scrapy.Field()
    flood_limit_water_level = scrapy.Field()

