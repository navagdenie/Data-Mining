# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import ParserItem
from scrapy.loader import ItemLoader

class YoulaSpider(scrapy.Spider):
    name = 'youla'
    allowed_domains = ['youla.ru']
    start_urls = ['https://youla.ru/all/nedvijimost/prodaja-doma?attributes[tip_postroyki][0]=10734']

    def parse(self, response):
        next_link = response.xpath('//div[@class="pagination__button"]/a/@href').extract_first()
        if next_link:
            yield response.follow(next_link, callback=self.parse)

        ads_link = response.xpath('//li[@class="product_item"]/a/@href').extract()
        for link in ads_link:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=ParserItem(), response=response)
        loader.add_xpath('title', '//h2[@class="sc-fjdhpX sc-hJwwgy lnNTjp"]/text()')
        loader.add_xpath('photos', '//div[@class="sc-bfYoXt sc-gbOuXE hwepLi"]/@src|//div[@class="sc-bfYoXt sc-gbOuXE hwepLi"]/img/@src')
        loader.add_xpath('house_square', '//li[@data-test-block="Attributes"]/dl/dd[1]/text()')
        loader.add_xpath('land_square', '//li[@data-test-block="Attributes"]/dl/dd[4]/text()')
        loader.add_xpath('material', '//li[@data-test-block="Attributes"]/dl/dd[2]/text()')
        loader.add_xpath('stairs', '//li[@data-test-block="Attributes"]/dl/dd[7]/text()')
        loader.add_xpath('address', '//span[@class="sc-bdVaJa OATzk"]/text()')
        loader.add_xpath('price', '//span[@class ="sc-gleUXh gfwvrl"]/text()')
        yield loader.load_item()