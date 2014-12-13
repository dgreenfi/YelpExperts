from pymongo import MongoClient
import numpy as np

client = MongoClient('Davids-MacBook-Air.local')
#access review database
db = client.yelp
collection = db.reviews_rest
#query for first date for each business id
cursor=collection.aggregate([{"$sort": { "business_id": 1, "date": 1 }} ,{"$group": {"_id": "$business_id", "avg_stars_calc":{ "$avg": "$stars" }}}],allowDiskUse=True)

avgs=[]
for id in cursor['result']:
   avgs.append(id)

collection = db.business
for x,avg in enumerate(avgs):
    collection.update({'business_id':avg['_id']},{'$set':{'avg_stars_calc':avg['avg_stars_calc']}})
    print x

__author__ = 'davidgreenfield'
