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
    # day1 = datetime(2017, 7, 13, 0, 0)
    # day2 = datetime(2016, 1, 1, 0, 0)
    # form = {
    #     '__EVENTVALIDATION': '',
    #     '__VIEWSTATE': '',
    #     'btn_query': '查询',
    #     'ddl_addvcd': '',
    #     'hidsearch': '',  # 81000880，81000755
    #     'txt_search': '',
    #     'txt_time1': (day1 - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
    #     'txt_time2': day1.strftime("%Y-%m-%d %H:%M")
    # }
    url = 'http://www.gdwater.gov.cn:9001/Report/WaterReport.aspx'

    def start_requests(self):
        yield Request(self.url, callback=self.parse)

    # def parse(self, response):
    #     soup = BS(response.body, 'lxml', from_encoding='utf-8')
    #     print(soup)
        # self.form['__EVENTVALIDATION'] = soup.find(
        #     'input', id='__EVENTVALIDATION')['value']
        # self.form['__VIEWSTATE'] = soup.find(
        #     'input', id='__VIEWSTATE')['value']
        # while self.day1 > self.day2:
        #     self.form['txt_time2'] = self.day1.strftime("%Y-%m-%d %H:%M")
        #     #print(self.day1.strftime("%Y-%m-%d %H:%M"))
        #     self.day1 = self.day1 - timedelta(hours=1)
        #     self.form['txt_time1'] = self.day1.strftime("%Y-%m-%d %H:%M")
        #     yield FormRequest(
        #         url=self.url, formdata=self.form, callback=self.second_parse, meta={'txt_time2': self.form['txt_time2']})

    def parse(self, response):
        soup = BS(response.body, "lxml", from_encoding='utf-8')
        # print(soup)
        # print(response.url)
    #     print('in')
    #     soup = BS(response.body, 'lxml')
        trs1 = soup.find('div', id='LeftTree').find_all('tr')
        # print(div)
        # tbody1 = div.find_all('tbody')
        # # print(tbody1)
        #
        # trs = divs.find_all('tr')
        # print(divs)
        self.count += 1
        trs1.reverse()
        trs1.pop()
        # # # print(trs)
        # # # print(trs)
        for tr in trs1:
            tds = tr.find_all('td')
             # print(tds)
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
        #     # print(response.meta['txt_time2'])
        #     # print(self.count)
            yield item

        trs2 = soup.find('div', id='RightTree').find_all('tr')
        # trs1 = tbody1[1].find_all('tr')
        # # trs = div.find_all('tr')
        trs2.reverse()
        trs2.pop()
        # trs1.pop()
        # # print(trs1)
        for tr in trs2:
            tds = tr.find_all('td')
            item = GdwaterItem()
            item['thread'] = 'Reservoir'
            item['city'] = tds[0].get_text().strip()
            item['county'] = tds[1].get_text().strip()
            item['site'] = tds[2].get_text().strip()
            item['time'] = tds[3].get_text().strip()
            item['water_level'] = tds[4].get_text().strip()
            item['flood_limit_water_level'] = tds[5].get_text().strip()
            print(item)
            # print(response.meta['txt_time2'])
            print(self.count)
            # print(item)
            yield item

