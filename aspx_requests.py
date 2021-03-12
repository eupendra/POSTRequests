import urllib
import scrapy
from scrapy import FormRequest, Request
import scraper_helper as sh
from scrapy.shell import inspect_response


class AspxSpider(scrapy.Spider):
    name = 'aspx'
    start_urls = ['https://www.unspsc.org/search-code']

    def parse(self, response, **kwargs):
        __VIEWSTATE = response.xpath('//*[@name="__VIEWSTATE"]/@value').get()
        __EVENTTARGET = response.xpath('//*[@name="__EVENTTARGET"]/@value').get()
        __EVENTARGUMENT = response.xpath('//*[@name="__EVENTARGUMENT"]/@value').get()
        __VIEWSTATEENCRYPTED = response.xpath('//*[@name="__VIEWSTATEENCRYPTED"]/@value').get()
        __VIEWSTATEGENERATOR = response.xpath('//*[@name="__VIEWSTATEGENERATOR"]/@value').get()
        __RequestVerificationToken = response.xpath('//*[@name="__RequestVerificationToken"]/@value').get()
        __dnnVariable = response.xpath('//*[@name="__dnnVariable"]/@value').get()
        form = {
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTTARGET': __EVENTTARGET if __EVENTTARGET else '',
            '__EVENTARGUMENT': __EVENTARGUMENT if __EVENTARGUMENT else '',
            '__VIEWSTATEENCRYPTED': __VIEWSTATEENCRYPTED,
            '__RequestVerificationToken': __RequestVerificationToken,
            '__dnnVariable': __dnnVariable,
            'dnn$ctr1535$UNSPSCSearch$txtsearchCode': '',
            'dnn$ctr1535$UNSPSCSearch$txtSearchTitle': 'organic',
            'dnn$ctr1535$UNSPSCSearch$btnSearch': 'Search',
        }

        yield FormRequest('https://www.unspsc.org/search-code',
                          formdata=form,
                          callback=self.parse_table)

    def parse_table(self, response):
        rows = response.xpath('//table[contains(@id, "gvDetailsSearchView")]//tr[td]')
        for row in rows:
            yield {
                'code': row.xpath('./td[1]/text()').get(),
                'value': row.xpath('./td[2]/text()').get()
            }
