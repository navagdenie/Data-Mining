from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import pandas as pd

user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

main_link_hh = 'https://www.hh.ru'
search_link_hh_begin = '/search/vacancy?area=1&st=searchVacancy&text='
search_link_hh_end = '&from=suggest_post'

main_link_sj = 'https://www.superjob.ru'
search_link_sj_begin = '/vacancy/search/?keywords='
search_link_sj_end = '&geo%5Bc%5D%5B0%5D=1'

def get_page_soup(url):
    page_data = requests.get(url, headers=user_agent)
    soup_data = bs(page_data.text, 'lxml')
    return soup_data

def get_salary(post):
    try:
        salary_text = post.find('div', class_='vacancy-serp-item__compensation')
        if salary_text is None:
            salary = {
                'salary_min': 0,
                'salary_max': 0
            }
        else:
            salary_text = salary_text.text.replace('\xa0', '').replace('от ', 'min').replace(' до ', 'max').replace(' ', 'cur')
            salary_min_t = salary_text.find('min')
            salary_max_t = salary_text.find('max')
            salary_cur_t = salary_text.find('cur')

            if salary_cur_t>0:
                salary_cur = salary_text[salary_cur_t:]
                salary_text = salary_text.replace(salary_cur, '')

            if salary_max_t>=0:
                if salary_min_t>=0:
                    salary_min = salary_text[(salary_min_t + 3):salary_max_t]
                else:
                    salary_min = 0
                salary_max = salary_text[(salary_max_t + 3):]
            else:
                if salary_min_t>=0:
                    salary_min = salary_text[(salary_min_t + 3):]
                else:
                    salary_min = 0
                salary_max = 0

            if len(salary_text)>0 and salary_min_t<0 and salary_max_t<0:
                sal = salary_text.find('-')
                salary_min = salary_text[:sal]
                salary_max = salary_text[(sal+1):]

            salary = {
                'salary_min': salary_min,
                'salary_max': salary_max
            }
    except:
        salary = {
            'salary_min': 0,
            'salary_max': 0
        }

    return salary

def get_page_strict_hh(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='vacancy-serp-item')

    for post in posts_data:

        salary = get_salary(post)
        post_dict = {
            'post_url': post.find('a').attrs.get('href'),
            'post_name': post.find('a').text,
            'post_salary_min': salary['salary_min'],
            'post_salary_max': salary['salary_max'],
            'post_website': main_link_hh
        }
        posts_list.append(post_dict)

    return posts_list

def get_salary_sj(post):
    try:
        salary_text = post.find('span', class_='_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz')
        if salary_text is None:
            salary = {
                'salary_min': 0,
                'salary_max': 0
            }
        else:
            salary_text = salary_text.text.replace('\xa0', '').replace('от', 'min').replace('до', 'max').replace('₽', '')
            salary_min_t = salary_text.find('min')
            salary_max_t = salary_text.find('max')
            salary_cur_t = salary_text.find('cur')

            if salary_cur_t>0:
                salary_cur = salary_text[salary_cur_t:]
                salary_text = salary_text.replace(salary_cur, '')

            if salary_max_t>=0:
                if salary_min_t>=0:
                    salary_min = salary_text[(salary_min_t + 3):salary_max_t]
                else:
                    salary_min = 0
                salary_max = salary_text[(salary_max_t + 3):]
            else:
                if salary_min_t>=0:
                    salary_min = salary_text[(salary_min_t + 3):]
                else:
                    salary_min = 0
                salary_max = 0

            if len(salary_text)>0 and salary_min_t<0 and salary_max_t<0:
                sal = salary_text.find('-')
                if sal<0:
                    sal = salary_text.find('—')

                if sal < 0:
                    salary_min = salary_text
                    salary_max = salary_text
                else:
                    salary_min = salary_text[:sal]
                    salary_max = salary_text[(sal + 1):]


            salary = {
                'salary_min': salary_min,
                'salary_max': salary_max
            }
    except:
        salary = {
            'salary_min': 0,
            'salary_max': 0
        }

    return salary

def get_page_strict_sj(soup):
    posts_list = []
    posts_data = soup.find_all('div', class_='_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr')

    for post in posts_data:
        try:
            post_url = post.find('a', attrs={'target':'_blank'}).attrs.get('href')
            post_name = post.find('div', class_='_3mfro CuJz5 PlM3e _2JVkc _3LJqf').text
        except:
            break

        salary = get_salary_sj(post)
        post_dict = {
            'post_url': f"{main_link_sj}{post_url}",
            'post_name': post_name,
            'post_salary_min': salary['salary_min'],
            'post_salary_max': salary['salary_max'],
            'post_website': main_link_sj
        }
        posts_list.append(post_dict)

    return posts_list

def parser(job_name, pages):

    job_name_hh = job_name.replace(' ', '+')
    search_link_hh = f"{main_link_hh}{search_link_hh_begin}{job_name_hh}{search_link_hh_end}"

    job_list = []
    for i in range(1, num_pages):

        soup_hh = get_page_soup(search_link_hh)
        job_list.extend(get_page_strict_hh(soup_hh))

        try:
            url_next = soup_hh.find('a', attrs={'rel': 'nofollow'}, text='дальше').attrs.get('href')
        except AttributeError as e:
            break
        search_link_hh = f"{main_link_hh}{url_next}"

    job_name_sj = job_name.replace(' ', '-').lower()
    search_link_sj = f"{main_link_sj}{search_link_sj_begin}{job_name_sj}{search_link_sj_end}"

    for i in range(1, num_pages):

        soup_sj = get_page_soup(search_link_sj)
        job_list.extend(get_page_strict_sj(soup_sj))

        try:
            url_next = soup_sj.find('a', attrs={'rel': 'next'}).attrs.get('href')
        except AttributeError as e:
            break
        search_link_hh = f"{main_link_sj}{url_next}"

    return job_list


if __name__ == '__main__':

    job_name = input('Введите название вакансии: ')

    pages = input('Введите количество страниц поиска: ')
    num_pages = int(pages)

    result_data = parser(job_name, pages)
    df = pd.DataFrame(result_data)
    pprint(result_data)