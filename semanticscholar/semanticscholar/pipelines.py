# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class SemanticscholarPipeline(object):
    titles_seen = []

    def process_item(self, item, spider):
        title = item['title']
        if title in self.titles_seen:
            raise DropItem("Duplicate item found!")
        else:
            self.titles_seen.append(title)
            return item
