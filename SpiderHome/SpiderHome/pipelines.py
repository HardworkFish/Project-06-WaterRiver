# -*- coding: utf-8 -*-
import multiprocessing
import os

import parse_type
import pymysql
import requests

from SpiderHome.store import GDSWDB, GdsqDB


class GdsqPipeline(object):
    def process_item(self, item, spider):
        spec = {'station': item['station'], 'time': item['time']}
        GdsqDB.djriver_.update(spec, {'$set': dict(item)}, upsert=True)
        return None


class GdwaterPipeline(object):
    def process_item(self, item, spider):
        spec = {
            'city': item['city'],
            'county': item['county'],
            'site': item['site'],
            'time': item['time']
        }
        thread = item.get('thread', None)
        item.pop('thread')
        GdsqDB[thread].update(spec, {'$set': dict(item)}, upsert=True)
        return None


class GdswPipeline(object):
    def process_item(self, item, spider):
        spec = {'tm': item['tm'], 'stcd': item['stcd'], 'stnm': item['stnm']}
        print(item['tm'])
        thread = item.get('thread', None)
        item.pop('thread')
        GDSWDB[thread].update(spec, {'$set': dict(item)}, upsert=True)
        return item

