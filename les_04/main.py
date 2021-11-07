from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
#from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
#import re
from lxml import html

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
yandex_news = db.yandex_news

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
response = requests.get('https://yandex.ru/news')
dom = html.fromstring(response.text)

info = dom.xpath('//article')

new_id = 1 # id из адреса не нашел, сама ссылка как понимаю тоже может различаться (разный id в конце записи), значит сами будем присваивать №, но корректно ли?
news_list = []
for i in info:
    news = {}
    name = i.xpath('.//h2[@class="mg-card__title"]/text()')[0]
    link = i.xpath('.//a[@class="mg-card__link"]/@href')[0]
    source = i.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
    time = i.xpath('.//span[@class="mg-card-source__time"]/text()')[0] # только время, без даты

    news['_id'] = new_id
    news['name'] = name
    news['link'] = link
    news['source'] = source
    news['time'] = time
    #print('Done!')
    news_list.append(news)
    try:
        yandex_news.insert_one(news)
    except dke:
        print(f"Документ с id = {news['_id']} уже существует в базе")
    new_id += 1
pprint(news_list)