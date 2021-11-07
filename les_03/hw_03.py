from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
import re

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_db']
hh_vac = db.hh_vacancy

Position = 'Python' #input('Ведите должность: ')
pages = 5 #int(input('Сколько страниц просмотреть (введите число): '))
salary_find = 10000 #int(input('Желаемая з.п.: '))

url = 'https://spb.hh.ru'
params = {'clusters': 'true',
          'area': '2',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'salary': None,
          'fromSearchLine': 'true',
          'text': Position,
          'from': 'suggest_post',
          'page': 0}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}


vacancys_list = []
while params['page'] < pages:
  response = requests.get(url + '/search/vacancy', params=params, headers=headers)
  dom = bs(response.text, 'html.parser')
  vacancys = dom.find_all('div', {'class': 'vacancy-serp-item'})

  if response.ok and vacancys:
    for vacancy in vacancys:
      vacansy_data = {}
      info = vacancy.find('a', {'class':'bloko-link'})
      link = info['href']
      id = re.findall("\d+", link)[0]  # id из ссылки
      name = info.text
      company = vacancy.find('div', {'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).text
      area = vacancy.find('div', {'class': 'bloko-text bloko-text_small bloko-text_tertiary'}).nextSibling.text
      try:
        salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).text
        s = salary.split()
        if ' – ' in salary:
            salary_min, salary_max, salary_cur = int(s[0]+s[1]), int(s[3]+s[4]), s[5]
        elif 'от' in salary:
            salary_min, salary_max, salary_cur = int(s[1] + s[2]), None, s[3]
        elif 'до' in salary:
            salary_min, salary_max, salary_cur = None, int(s[1] + s[2]), s[3]
        else:
            salary_min, salary_max, salary_cur = int([0] + s[1]), int(s[0] + s[1]), s[2]
      except:
        salary_min, salary_max, salary_cur = None, None, None
        continue
      vacansy_data['_id'] = id
      vacansy_data['name'] = name
      vacansy_data['company'] = company
      vacansy_data['area'] = area
      vacansy_data['link'] = link
      vacansy_data['salary_min'] = salary_min
      vacansy_data['salary_max'] = salary_max
      vacansy_data['salary_cur'] = salary_cur
      #vacancys_list.append(vacansy_data)
      #print(f"Обработанно {params['page']+1} страниц(ы)")
      #params['page'] += 1
      if (salary_min and salary_min >= salary_find) or (salary_min is None and salary_max and salary_max >= salary_find):
        try:
            hh_vac.insert_one(vacansy_data)
        except dke:
            print(f"Документ с id = {vacansy_data['_id']} уже существует в базе")
      else:
            continue
      params['page'] += 1
  else:
      break

print('End')
for item in hh_vac.find():
     pprint(item)
