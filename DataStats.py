from pymongo import MongoClient
from bson.son import SON
from datetime import date
from datetime import datetime
import numpy as np
client = MongoClient('Davids-MacBook-Air.local')
dir='/Users/davidgreenfield/socialfinalproject/'

#full file
db = client.yelp
# create ages
collection = db.reviews_rest
cursor = collection.find({},{'date','business_id','stars'})
rev_list=[]
for rec in cursor:

    rev_list.append((rec['business_id'],rec['date'],rec['stars']))

db = client.yelp
collection = db.review_starts
cursor_s = collection.find()
sd_lookup={}
for sd in cursor_s:
    #print sd
    sd_lookup[sd['_id']]=sd['first_review']


ages=[]
ratings=[]
for rec in rev_list:
    #print sd_lookup[rec[0]],rec[1]
    fd=datetime.strptime(sd_lookup[rec[0]], '%Y-%m-%d')
    rd=datetime.strptime(rec[1], '%Y-%m-%d')
    #print (rd-fd).days
    ratings.append(rec[2])
    ages.append(((rd-fd).days))

thefile=open(dir+'rev_ages.txt','w+')
for item in ages:
  thefile.write("%s\n" % item)

thefile=open(dir+'rev_ratings.txt','w+')
for item in ratings:
  thefile.write("%s\n" % item)

#numpy.histogram(ages)

__author__ = 'davidgreenfield'
