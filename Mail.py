from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument('--headless')

mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client.mail
collection = db.mails

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://mail.ru/')
assert 'Mail.ru' in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172')

elem.send_keys(Keys.RETURN)


pass_elem = WebDriverWait(driver,60).until(
          EC.element_to_be_clickable((By.ID, 'mailbox:password'))
        )
pass_elem.send_keys('NewPassword172')

pass_elem.send_keys(Keys.RETURN)
assert 'Mail.ru' in driver.title

link_begin = 'https://e.mail.ru/messages/inbox/?page='
n=2
mail_list=[]
while True:
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="js-href b-datalist__item__link"]'))
            )
        elements = driver.find_elements_by_xpath('//a[@class="js-href b-datalist__item__link"]')
        for elem in elements:
            mail_list.append(elem.get_attribute('href'))

        driver.get(f'{link_begin}{n}')
        print(f'Page: {n}   URL: {link_begin}{n}')
        if driver.current_url != f'{link_begin}{n}':
            break
        n += 1
    except:
        break

for elem in mail_list:
    driver.get(elem)
    mail_from = driver.find_element(By.XPATH, '//span[@class="b-contact-informer-target js-contact-informer"]').get_attribute('data-contact-informer-email')
    mail_date = driver.find_element(By.CLASS_NAME, 'b-letter__head__date').text
    if mail_date.find('сегодня, ')>-1:
        mail_date = mail_date.replace('сегодня, ', '')
        mail_date = datetime.strptime(f'{datetime.date(datetime.now())} {mail_date}', "%Y-%m-%d %H:%M")
    else:
        mail_date = mail_date.replace(',', '').replace('января', '1').replace('февраля', '2').replace('марта', '3').replace('апреля', '4').replace('мая', '5').replace('июня', '6').replace('июля', '7').replace('августа', '8').replace('сентября', '9').replace('октября', '10').replace('ноября', '11').replace('декабря', '12')
        mail_date = datetime.strptime(mail_date, "%d %m %Y %H:%M")
    mail_title = driver.find_element(By.CLASS_NAME, 'b-letter__head__subj__text').text
    mail_body = driver.find_element(By.XPATH, '//div[@class="js-helper js-readmsg-msg"]').text
    item = {
        'link': elem,
        'mail_from': mail_from,
        'mail_date': mail_date,
        'mail_title': mail_title,
        'mail_body': mail_body
    }

    if collection.count_documents({'link': elem}) == 0:
        collection.insert_one(item)

driver.quit()