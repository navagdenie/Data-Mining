# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Data+scientist&from=suggest_post']

    def parse(self, response:HtmlResponse):
        link_next = response.xpath('//a[@class="bloko-button HH-Pager-Controls-Next HH-Pager-Control"]/@href').extract_first()
        if link_next:
            yield response.follow(link_next, callback=self.parse)

        list_items = response.xpath('//a[@class="bloko-link HH-LinkModifier"]/@href').extract()
        for item in list_items:
            yield response.follow(item, callback=self.parse_item)

    def parse_item(self, response:HtmlResponse):

        name = response.xpath('//h1[@data-qa="vacancy-title"]/text()|//h1[@data-qa="vacancy-title"]/span/text()').extract()
        min_salary = response.xpath('//span[@itemprop="baseSalary"]/*/meta[@itemprop="minValue"]/@content').extract_first()
        max_salary = response.xpath('//span[@itemprop="baseSalary"]/*/meta[@itemprop="maxValue"]/@content|'
                                    '//span[@itemprop="baseSalary"]/*/meta[@itemprop="value"]/@content').extract_first()
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




