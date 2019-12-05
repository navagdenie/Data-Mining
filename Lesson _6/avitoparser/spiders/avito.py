# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import ParserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva_i_mo/doma_dachi_kottedzhi/prodam/kottedzh?cd=1']

    def parse(self, response:HtmlResponse):
        next_link = response.xpath('//a[@class="snippet-link"]/@href').extract_first()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

        ads_link = response.xpath('//a[@class="snippet-link"]/@href').extract()
        for link in ads_link:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=ParserItem(), response=response)
        loader.add_xpath('title', '//span[@class="title-info-title-text"]/text()')
        loader.add_xpath('photos', '//div[@class="gallery-img-frame js-gallery-img-frame"]/@data-url')
        loader.add_xpath('house_square', '//li[@class="item-params-list-item"][1]/text()[2]')
        loader.add_xpath('land_square', '//li[@class="item-params-list-item"][2]/text()[2]')
        loader.add_xpath('material', '//li[@class="item-params-list-item"][4]/text()[2]')
        loader.add_xpath('stairs', '//li[@class="item-params-list-item"][6]/text()[2]')
        loader.add_xpath('address', '//span[@class="item-address__string"]/text()')
        loader.add_xpath('price', '//span[@class ="js-item-price"]/@content')

        yield loader.load_item()
