
from pymongo import MongoClient
import numpy as np

client = MongoClient('Davids-MacBook-Air.local')

db = client.yelp
collection = db.review_starts
cursor = collection.find({})
rev_list=[]
for rec in cursor:
    rev_list.append(rec)
print len(rev_list)
biz_list=[]
collection = db.business
cursor = collection.find({},{'_id'})
for rec in cursor:
    biz_list.append(rec)

collection = db.business
#for business in rev_list:
 ##  print business['_id']
   # print collection.find_one({'business_id':business['_id']})

for business in rev_list:
    collection.update({'business_id':business['_id']},{'$set':{'first_review':business['first_review']}})

__author__ = 'davidgreenfield'
