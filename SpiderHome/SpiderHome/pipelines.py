from SpiderHome.store import GDSWDB,  GdsqDB


class GdsqPipeline(object):
    def process_item(self, item, spider):
        # spec = {'station': item['station'], 'time': item['time']}
        # GdsqDB.djriver.update(spec, {'$set': dict(item)}, upsert=True)
        year = 'djriver-' + item['year']
        item.pop('year')
        GdsqDB[year].insert(dict(item))
        return None


class GdwaterPipeline(object):
    def process_item(self, item, spider):
        # spec = {
        #     'city': item['city'],
        #     'county': item['county'],
        #     'site': item['site'],
        #     'time': item['time']
        # }
        thread = item.get('thread', None)
        item.pop('thread')
        # GdsqDB[thread].update(spec, {'$set': dict(item)}, upsert=True)

        # thread = item.get('thread', None)
        GdsqDB[thread].insert(dict(item))
        return None

#
# class GdswPipeline(object):
#     def process_item(self, item, spider):
#         # spec = {
#         #     'tm': item['tm'],
#         #     'stcd': item['stcd'],
#         #     'stnm': item['stnm']
#         # }
#         # print(item['tm'])
#         thread = item.get('thread', None)
#         # item.pop('thread')
#         # GDSWDB[thread].update(spec, {'$set': dict(item)}, upsert=True)
#         GDSWDB[thread].insert(item)
#
#         return item

