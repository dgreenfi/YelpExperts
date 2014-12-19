from pymongo import MongoClient
import networkx as nx
import datetime
import operator
import numpy as np
from datetime import timedelta
from pprint import pprint

client = MongoClient('Davids-MacBook-Air.local')
db = client.yelp

####### Load Business lookup #####
business={}
collection = db.business
cursor = collection.find({"avg_stars_calc":{"$gt":0}})
for bus in cursor:
    business[bus['business_id']]=bus

####### Load Review lookup #####
reviews={}
collection = db.reviews_rest
cursor = collection.find({})
for rev in cursor:
    if rev['user_id'] in reviews.keys():
        reviews[rev['user_id']].append(rev)
    else:
        reviews[rev['user_id']]=[rev]



collection = db.user
#cursor=collection.find({})

bulk = db.user.initialize_unordered_bulk_op()
for user in reviews:
    collection = db.reviews_rest
    #cursor=collection.find({"user_id":user["user_id"]})
    review_ratings=[]
    rest_ratings=[]
    for num,review in enumerate(reviews[user]):
        print user
        print review
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        if bus_start+timedelta(days=150)>rev_date:
            if bus_start<datetime.datetime.strptime("2013-01-01", "%Y-%m-%d").date():
                try:
                    rest_ratings.append(business[review["business_id"]]["avg_stars_calc"])
                    review_ratings.append(review["stars"])
                except:
                    pass

    collection = db.user
    print review_ratings,rest_ratings
    bulk.find({'user_id':user}).update({'$set':{'review_ratings':review_ratings,"rest_ratings":rest_ratings}})
result = bulk.execute()
pprint(result)

__author__ = 'davidgreenfield'
