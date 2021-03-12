import scrapy
from scrapy import FormRequest, Request


class LoginSpider(scrapy.Spider):
    name = 'login'

    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        form = {
            'csrf_token': response.xpath('//*[@name="csrf_token"]/@value').get(),
            'username': '1',
            'password': '1',
        }
        r = FormRequest.from_response(response,
                                      formdata=form,
                                      callback=self.after_login)
        yield r

    def after_login(self, response):
        if response.xpath('//a[text()="Logout"]'):
            print('logged in')
        else:
            print('NOT logged in')
