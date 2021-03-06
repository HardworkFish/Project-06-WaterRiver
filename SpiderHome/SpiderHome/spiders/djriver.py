from datetime import date, timedelta
from re import findall, sub

from bs4 import BeautifulSoup as BS
from scrapy import Request
from scrapy.spiders import Spider

from  SpiderHome.items import GdsqItem


class GdsqSpider(Spider):
    name = 'djriver'
    today = date.today()
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GdsqPipeline': 300,
        }
    }

    def start_requests(self):
        # crawl_day = date.today() - timedelta(7)
        # while crawl_day < self.today:
        #     url = 'http://www.djriver.cn/xxfb/sqyq_cen.asp?page=1&jctime=%s&jctime1=%s&zm=' % (
        #         str(crawl_day), str(crawl_day))
        #     yield Request(url, callback=self.parse)
        #     crawl_day = crawl_day + timedelta(1)
        # url = 'http://www.djriver.cn/xxfb/sqyq_cen.asp?page=1&jctime=%s&jctime1=%s&zm=' % (
        #         '2008-09-01', '2008-12-31')
        for i in range(2009, 2010):
            url = 'http://www.djriver.cn/xxfb/sqyq_cen.asp?page=1&jctime=%s-09-01&jctime1=%s-12-31&zm=' % (
                i, i)
            yield Request(url, meta={'year': str(i)},  callback=self.parse)

    def parse(self, response):
        year = response.meta['year']
        soup = BS(response.body, 'lxml', from_encoding='utf-8')

        now_page = int(findall('\\d+', response.url)[0])
        # print(now_page)
        if len(
                findall(
                    '\d+',
                    soup.find(
                        'td', class_="ifont1", attrs={'colspan': '5'})
                            .get_text().split('\t')[0].strip().split('\u3000')[
                        -1])) == 0:
            return
        page = int(
            findall(
                '\d+',
                soup.find(
                    'td', class_="ifont1", attrs={'colspan': '5'}).get_text()
                    .split('\t')[0].strip().split('\u3000')[-1])[0])
        print(page)
        trs = soup.find_all('table')[1].find_all('tr')
        trs.pop()
        trs.reverse()
        trs.pop()
        trs.pop()
        trs.pop()
        for tr in trs:
             item = GdsqItem()
             tds = tr.find_all('td')
             item['year'] = year
             item['station'] = tds[0].get_text().strip()
             item['time'] = tds[1].get_text().strip()
             item['water_level'] = tds[2].get_text().strip()
             item['flow'] = tds[3].get_text().strip()
             item['warning_water_level'] = tds[4].get_text().strip()
             print(item)
             yield item
        if now_page < page:
             url = sub('page=\\d+', 'page=%d' % (now_page + 1), response.url)
             yield Request(url,  meta={'year': year}, callback=self.parse)




        ############ yes, yes, yes 2018-10-10ll
