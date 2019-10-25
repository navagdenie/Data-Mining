# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

class HhVacSpSpider(scrapy.Spider):
    name = 'hh_vac_sp'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Data+scientist&from=suggest_post']

    def parse(self, response:HtmlResponse):
        pagination = response.css('div.bloko-gap.bloko-gap_top a.bloko-button.HH-Pager-Controls-Next.HH-Pager-Control::attr(href)').extract()
        next_link = pagination[-1]
        yield response.follow(next_link, callback=self.parse)

        blog_pages = response.css('div.vacancy-serp-item__row.vacancy-serp-item__row_header a.bloko-link.HH-LinkModifier::attr(href)').extract()
        for itm in blog_pages:
            yield response.follow(itm, callback=self.parse_blog_page)

    def get_company_url(self, response:HtmlResponse):
        website = response.css('div.HH-SidebarView-UrlContainer a.company-url::attr(href)').extract_first()
        return website

    def parse_blog_page(self, response: HtmlResponse):
        title = response.css('div.vacancy-title h1.header::text').extract()
        company_name = response.css('p.vacancy-company-name-wrapper a.vacancy-company-name span::text').extract()
        company_link = response.css('p.vacancy-company-name-wrapper a.vacancy-company-name::attr(href)').extract()
        salary = response.css('div.vacancy-title p.vacancy-salary::text').extract()

        skills_list = []
        skills = response.css('div.vacancy-section span.Bloko-TagList-Text::text').extract()
        for itm in skills:
            skills_list.append(itm)

        #company_url = response.follow(company_link, callback=self.get_company_url)

        yield {
            'title': title,
            'company_name': company_name,
            'company_link': company_link,
            'salary': salary,
            #'company_url': company_url,
            'skills_list': skills_list
        }



        print(1)
