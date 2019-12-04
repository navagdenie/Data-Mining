# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pprint

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.job_base

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]

        job_item = {
            'name':item['data']['name'],
            'min_salary':item['data']['min_salary'],
            'max_salary':item['data']['max_salary'],
            'link':item['data']['link'],
            'source':item['data']['source'][0]
        }

        if spider.name == 'sjru':
            salary_text = job_item['min_salary'][0]
            salary_text = salary_text.replace('<span class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc">', '').replace('\xa0', '')
            salary_text = salary_text.replace('<!--', '').replace('-->', '').replace('<span>', '').replace('</span>', '')

            if salary_text is None:
                salary_min = 0
                salary_max = 0

            else:
                salary_text = salary_text.replace('\xa0', '').replace('от', 'min').replace('до', 'max').replace('₽', '')
                salary_min_t = salary_text.find('min')
                salary_max_t = salary_text.find('max')
                salary_cur_t = salary_text.find('cur')

                if salary_cur_t > 0:
                    salary_cur = salary_text[salary_cur_t:]
                    salary_text = salary_text.replace(salary_cur, '')

                if salary_max_t >= 0:
                    if salary_min_t >= 0:
                        salary_min = salary_text[(salary_min_t + 3):salary_max_t]
                    else:
                        salary_min = 0
                    salary_max = salary_text[(salary_max_t + 3):]
                else:
                    if salary_min_t >= 0:
                        salary_min = salary_text[(salary_min_t + 3):]
                    else:
                        salary_min = 0
                    salary_max = 0

                if len(salary_text) > 0 and salary_min_t < 0 and salary_max_t < 0:
                    sal = salary_text.find('-')
                    if sal < 0:
                        sal = salary_text.find('—')

                    if sal < 0:
                        salary_min = salary_text
                        salary_max = salary_text
                    else:
                        salary_min = salary_text[:sal]
                        salary_max = salary_text[(sal + 1):]

            job_item['min_salary'] = salary_min.replace(' ', '')
            job_item['max_salary'] = salary_max.replace(' ', '').replace('говорённости', '0')

        if collection.count_documents({'link':item['data']['link']}) == 0:
            collection.insert_one(job_item)

        return item





