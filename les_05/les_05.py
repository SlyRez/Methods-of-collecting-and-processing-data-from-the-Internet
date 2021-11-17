from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pymongo.errors import DuplicateKeyError as dke
import requests
from lxml import html
from pprint import pprint

# настройки
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

# Монго ДБ
client = MongoClient('127.0.0.1', 27017)
db = client['mails_db']
mails_db = db.mails_db

# авторизация
elem = driver.find_element(By.NAME, 'login')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)
# time.sleep(1)
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.element_to_be_clickable((By.NAME, 'password')))
# elem = driver.find_element(By.NAME, 'password')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

# выбор 1го письма
time.sleep(3)
elem = driver.find_element(By.CLASS_NAME,'llc_normal')
elem.click()

# анализ письма
#new_id = 1
mails_list = []
#def parse_mail():
mails = {}
time.sleep(5)
mail_from = driver.find_element(By.CLASS_NAME, "letter-contact").text
mail_datetime = driver.find_element(By.CLASS_NAME, "letter__date").text
mail_theme = driver.find_element(By.CLASS_NAME, "thread__subject-line").text
mail_content = driver.find_element(By.CLASS_NAME, "letter__body").text
mails['mail_from'] = mail_from
mails['mail_datetime'] = mail_datetime
mails['mail_theme'] = mail_theme
mails['mail_content'] = mail_content
mails_list.append(mails)
print('Done!!!')
try:
    mails_db.insert_one(mails)
except dke:
    print(f"Документ с id = {mails['_id']} уже существует в базе")
#new_id += 1

# следующее письмо
time.sleep(1)
body = driver.find_element(By.TAG_NAME, "body")
print(body)
body.send_keys(Keys.CONTROL, Keys.DOWN)






#driver.quit()



