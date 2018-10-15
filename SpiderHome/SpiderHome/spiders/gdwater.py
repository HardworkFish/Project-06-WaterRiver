# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from re import findall, sub
from time import sleep

from bs4 import BeautifulSoup as BS
from scrapy import Request
from scrapy.http import FormRequest
from scrapy.spiders import Spider

from SpiderHome.items import GdwaterItem


class GdwaterSpider(Spider):
    name = 'gdwater'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GdwaterPipeline': 300,
        },
    }
    count = 0
    url = 'http://www.gdwater.gov.cn:9001/Report/WaterReport.aspx'

    def start_requests(self):
        yield Request(self.url, callback=self.parse)

    def parse(self, response):
        soup = BS(response.body, "lxml", from_encoding='utf-8')
        trs1 = soup.find('div', id='LeftTree').find_all('tr')
        self.count += 1

        for tr in trs1[2:]:
            tds = tr.find_all('td')
            item = GdwaterItem()
            item['thread'] = 'river'
            item['city'] = tds[0].get_text().strip()
            item['county'] = tds[1].get_text().strip()
            item['site'] = tds[2].get_text().strip()
            item['time'] = tds[3].get_text().strip()
            item['water_level'] = tds[4].get_text().strip()
            item['warning_level'] = tds[5].get_text().strip()
            item['water_potemtial'] = tds[6].get_text().strip()
            print(item)
            yield item

        trs2 = soup.find('div', id='RightTree').find_all('tr')

        for tr in trs2[2:]:
            tds = tr.find_all('td')
            item = GdwaterItem()
            item['thread'] = 'Reservoir'
            item['city'] = tds[0].get_text().strip()
            item['county'] = tds[1].get_text().strip()
            item['site'] = tds[2].get_text().strip()
            item['time'] = tds[3].get_text().strip()
            item['water_level'] = tds[4].get_text().strip()
            item['flood_limit_water_level'] = tds[5].get_text().strip()
            yield item

