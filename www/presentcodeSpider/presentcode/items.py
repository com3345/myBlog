# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PresentCodeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    presentcode = scrapy.Field()
    timestr = scrapy.Field()
    url = scrapy.Field()
    endtimestamp = scrapy.Field()
