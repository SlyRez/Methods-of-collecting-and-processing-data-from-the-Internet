# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacansies1711']

    def process_item(self, item, spider):

        if item['salary']:
            item['salary'] = self.process_salary(item['salary'])

        name = item['name']
        salary_min = item['salary'][0]
        salary_max = item['salary'][1]
        salary_cur = item['salary'][2]
        link = item['url']

        vacancy_item = {'vacancy_name': name, 'salary_min': salary_min,
                        'salary_max': salary_max, 'salary_currency': salary_cur,
                        'vacancy_link': link}

        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_item)
        #collection.update_one({'vacancy_link': vacancy_item['vacancy_link']}, {'$set': vacancy_item}, upsert=True)
        return vacancy_item



    def process_salary (self, salary):
        salary_min = None
        salary_max = None
        salary_cur = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        if salary[0] == "з/п не указана" or salary[0] == "По договорённости":
            salary_min = None
            salary_max = None
            salary_cur = None
        elif salary[0] == "до":
            salary_min = None
            salary_max = salary[2]
            salary_cur = salary[-1]
        elif len(salary) == 3 and salary[0].isdigit():
            salary_min = None
            salary_max = salary[0]
            salary_cur = salary[-1]
        elif salary[0] == "от":
            salary_min = salary[2]
            salary_max = None
            salary_cur = salary[-1]
        elif len(salary) > 3 and salary[0].isdigit():
            salary_min = salary[0]
            salary_max = salary[2]
            salary_cur = salary[-1]

        result = [salary_min, salary_max, salary_cur]
        return result
