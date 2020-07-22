
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client['insta']

print('Подписчики:')
print()
foloowers = db.followers #запрос подписчиков
foloowers_list = foloowers.find({'user_id': '8729638151'})
#foloowers_list = foloowers.find()
for follower in foloowers_list:
    print(follower['full_name_follower']+' '+follower['follower'])
print()
print('Подписки:')
print()
foloowing = db.following #запрос подписок
foloowing_list = foloowing.find({'user_id': '8729638151'})
for following in foloowing_list:
    print(following['full_name_follower']+' '+following['follower'])