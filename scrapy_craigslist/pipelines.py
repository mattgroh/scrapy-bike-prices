# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):

    def __init__(self):
        self.post_id_seen = set()

    def process_item(self, item, spider):
        if item['post_id'] in self.post_id_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.post_id_seen.add(item['post_id'])
            return item
