# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SemanticscholarItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    year = scrapy.Field()
    authors = scrapy.Field()
    refs = scrapy.Field()
