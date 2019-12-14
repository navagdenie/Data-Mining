# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response:HtmlResponse):
        link_next = response.xpath('//a[@rel="next"][last()]/@href').extract_first()
        if link_next:
            yield response.follow(link_next, callback=self.parse)

        list_items = response.xpath('//div[@class="_2g1F-"]/a[@target="_blank"]/@href').extract()
        for item in list_items:
            yield response.follow(item, callback=self.parse_item)

    def parse_item(self, response:HtmlResponse):

        name = response.xpath('//h1[@class="_3mfro rFbjy s1nFK _2JVkc"]/text()|//span[@class="_1rS-s"]/text()').extract()
        min_salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]').extract()
        max_salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]').extract()
        link = response.url
        source = self.allowed_domains

        #print(name, min_salary, max_salary, link, source)

        job_data = {
            'name':name,
            'min_salary':min_salary,
            'max_salary':max_salary,
            'link':link,
            'source':source
        }

        yield JobparserItem(data = job_data)




