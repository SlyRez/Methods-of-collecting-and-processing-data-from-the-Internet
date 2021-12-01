from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
mongo_base = client['instagram_scrapy']

collection = mongo_base['instagram']
users_db = collection.distinct('source_name')

print(f'Users in DB :  {users_db}')
user = input("Enter username: ")

print(f'\nSubscribers list {user}:')
for item in collection.find({'source_name': user, 'subs_type': 'subscriber'}):
    pprint({item['user_name']})

print('\n')
print('-'*50)
print('\n')

print(f'\nSubscriptions list {user}:')
for item in collection.find({'source_name': user, 'subs_type': 'subscription'}):
    pprint({item['user_name']})
