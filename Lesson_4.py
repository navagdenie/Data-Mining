import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

def mail_parser(collection, news_list):

    request_mail = requests.get('https://mail.ru/', headers=user_agent).text
    root_mail = html.fromstring(request_mail)

    mail_news = root_mail.xpath('//div[@class="news-item o-media news-item_media news-item_main"]|'
                                '//div[@class="news-item i-fade-white i-fade-full i-nowrap news-item_inline news-item_inline-first"]|'
                                '//div[@class="news-item i-fade-white i-fade-full i-nowrap news-item_inline"]')

    for item in mail_news:
        link = item.xpath('.//a[@target][last()]/@href')
        request_link = requests.get(link[0], headers=user_agent).text
        root = html.fromstring(request_link)

        header = root.xpath('//h1[@class="hdr__inner"]/text()')
        post_date = root.xpath('//span[@class="note__text breadcrumbs__text js-ago"]/@datetime')
        source = root.xpath('//a[@class="link color_gray breadcrumbs__link"]/@href')

        post_dict = {
            'header': header,
            'link': link[0],
            'post_date': post_date,
            'source': source
        }

        news_list.append(post_dict)

        if collection.count_documents({'link': link[0]}) == 0:
            collection.insert_one(post_dict)

def lenta_parser(collection, news_list):

    lenta_link = 'https://lenta.ru/'
    request_lenta = requests.get(lenta_link, headers=user_agent).text
    root_lenta = html.fromstring(request_lenta)

    lenta_news = root_lenta.xpath('//div[@class="span4"]/div[@class="item"]|//div[@class="span4"]/div[@class="first-item"]')

    for item in lenta_news:
        link = item.xpath('.//a/@href')
        header = item.xpath('.//a/text()')
        post_date = item.xpath('.//time/@datetime')
        source = lenta_link

        post_dict = {
            'header': header.replace('\xa0', ''),
            'link': f"{lenta_link[:-1]}{link[0]}",
            'post_date': post_date,
            'source': source
        }

        news_list.append(post_dict)

        if collection.count_documents({'link': link}) == 0:
            collection.insert_one(post_dict)

def yandex_parser(collection, news_list):

    yandex_link = 'https://yandex.ru/news/'
    request_yandex = requests.get(yandex_link, headers=user_agent).text
    root_yandex = html.fromstring(request_yandex)

    yandex_news = root_yandex.xpath('//div[@class="story__topic"]')

    for item in yandex_news:
        link = item.xpath('.//a/@href')[-1]
        header = item.xpath('.//a/text()')[-1]
        text_date = item.xpath('..//div[@class="story__date"]/text()')
        post_date = text_date[0][-5:]
        source = text_date[0][:-5]

        post_dict = {
            'header': header,
            'link': f"{yandex_link[:-6]}{link}",
            'post_date': post_date,
            'source': source.replace(' ', '')
        }

        news_list.append(post_dict)

        if collection.count_documents({'link': link}) == 0:
            collection.insert_one(post_dict)

if __name__ == '__main__':

    mongo_url = 'mongodb://localhost:27017'
    client = MongoClient(mongo_url)
    db = client.news
    collection = db.news

    news_list = []
    mail_parser(collection, news_list)
    lenta_parser(collection, news_list)
    yandex_parser(collection, news_list)

    pprint(news_list)



