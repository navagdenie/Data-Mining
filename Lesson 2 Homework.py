import requests
from bs4 import BeautifulSoup
import datetime as DT
import json

domain_url = 'https://geekbrains.ru/'
blog_url = 'https://geekbrains.ru/posts'

def get_pade_soup(url):
    page_data = requests.get(url)
    soup_data = BeautifulSoup(page_data.text, 'lxml')
    return soup_data

def get_post_strict(url):
    post_soup = get_pade_soup(url)

    post_dict = {
        'post_title': post_soup.find('h1').text,
        'post_subtitle': post_soup.find('div', class_='blogpost-description').text,
        'post_image': post_soup.find('img').attrs.get('src'),
        'post_text': post_soup.find('div', class_='blogpost-content content_text content js-mediator-article').attrs.get('content'),
        'post_date': DT.datetime.fromisoformat(post_soup.find('time').attrs.get('datetime')).timestamp(),
        'post_author': {
            'author_name': post_soup.find('div', class_='col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v').find('div', class_='text-lg text-dark').text,
            'author_link': f"{domain_url}{post_soup.find('div', class_='col-md-5 col-sm-12 col-lg-8 col-xs-12 padder-v').find('a').attrs.get('href')}"
        }
    }

    return post_dict

def get_page_strict(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='post-item')

    for post in posts_data:
        post_url = f"{domain_url}{post.find('a').attrs.get('href')}"
        post_dict = get_post_strict(post_url)
        posts_list.append(post_dict)

    return posts_list

def parser(url):
    posts_list = []
    while True:
        soup = get_pade_soup(url)
        posts_list.extend(get_page_strict(soup))
        try:
            url_next = soup.find('a', attrs={'rel': 'next'}, text='›').attrs.get('href')
        except AttributeError as e:
            break
        url = f"{domain_url}{url_next}"
    return posts_list


result_data = parser(blog_url)

with open('posts.json', 'w') as f:
    json.dump(result_data, f)

