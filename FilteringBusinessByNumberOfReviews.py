from pymongo import MongoClient
import datetime
from datetime import timedelta

import numpy as np


client = MongoClient('Davids-MacBook-Air.local')
# First, group reviews by business id.
# db.reviews_rest.aggregate([{ $group :{ _id : "$business_id"}}])

db = client.yelp
collection = db.reviews_rest

cursor = collection.aggregate([{"$group": {"_id": "$business_id"}}])

#print (cursor)
threshold = 30

highFreqBusiness = {}
for business in cursor['result']:
    bId = business['_id']
    # Then, get their counts and check if they are above a threshold
    #> db.reviews_rest.count({"business_id":"5se9c1ggSm2oMrnWO3ZSgw"})
    rev_count = collection.find({"business_id":bId}).count()
    if rev_count > threshold:
        highFreqBusiness[bId] = rev_count
    print bId,rev_count

print len(highFreqBusiness)



collection = db.freqBusiness

for key,value in highFreqBusiness.iteritems():
    business = db.business.find({"business_id":key})
    collection.insert(business)











__author__ = 'karanmatnani'
