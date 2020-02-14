# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.crawler import CrawlerProcess


class XSpider(scrapy.Spider):

    name = 'x_collector'

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.results = {}
        self.body = {
            'SEARCH_VALUE': 'X',
            'STARTS_WITH_YN': 'true',
            'ACTIVE_ONLY_YN': 'true'
        }  # search businesses that start with X and are active

    def start_requests(self):
        '''
        Queries records using self.body
        '''
        yield scrapy.http.JsonRequest(
            'https://firststop.sos.nd.gov/api/Records/businesssearch',
            callback=self.parse_businesssearch,
            data=self.body)

    def parse_businesssearch(self, response):
        '''
        start_requests() request callback
        Queries for additional information for each entry from start_requests()
        response json and stores it in self.results
        '''
        jsonresponse = json.loads(response.text)
        for k, v in jsonresponse['rows'].items():
            self.results[k] = {
                'Business Name': v['TITLE'][0],
            }
            yield scrapy.http.JsonRequest(
                'https://firststop.sos.nd.gov/api/FilingDetail/business/' + k +
                '/false',
                callback=self.parse_business,
                cb_kwargs={'row_id': k},
                method='GET')

    def parse_business(self, response, row_id):
        '''
        parse_businesssearch() request callback
        Extracts information from parse_businesssearch() response json and
        stores it in self.results
        '''
        json_response = json.loads(response.text)
        current = self.results[row_id]
        detail_list = json_response['DRAWER_DETAIL_LIST']
        for item in detail_list:
            current[item['LABEL']] = item['VALUE']

    @staticmethod
    def close(spider, reason):
        '''
        Writes self.results to file on spider close
        '''
        with open('xspider_data.json', 'w', encoding='utf-8') as f:
            json.dump(spider.results, f, ensure_ascii=False)
        super().__close(spider, reason)


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'CLOSESPIDER_ITEMCOUNT': 196,
        'DOWNLOAD_DELAY': 1
    })
    process.crawl(XSpider)
    process.start()
