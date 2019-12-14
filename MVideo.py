from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
import json

chrome_options = Options()
chrome_options.add_argument('start-maximized')
#chrome_options.add_argument('--headless')

mongo_url = 'mongodb://localhost:27017'
client = MongoClient(mongo_url)
db = client.MVideo
collection = db.hits

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
assert 'М.Видео' in driver.title

while True:
    next_page = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.accessories-new .sel-hits-button-next'))
    )
    if next_page.get_attribute('class').find('disabled')>-1:
        break
    time.sleep(10)
    next_page.click()


wrapper = driver.find_element(By.CSS_SELECTOR, '.accessories-new')
elements = wrapper.find_elements(By.CSS_SELECTOR, '.gallery-list-item')
for el in elements:
    pic = el.find_element(By.CLASS_NAME, 'c-product-tile-picture')
    a = pic.find_element(By.XPATH, '//a[@data-product-info]')
    link = a.get_attribute('href')
    item = json.loads(a.get_attribute('data-product-info'))
    item['link'] = link

    if collection.count_documents({'link': link}) == 0:
        collection.insert_one(item)

driver.quit()