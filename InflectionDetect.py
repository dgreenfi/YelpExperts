from pymongo import MongoClient
import datetime
from datetime import timedelta

import numpy as np

client = MongoClient('Davids-MacBook-Air.local')
dir='/Users/davidgreenfield/socialfinalproject/'

db = client.yelp
collection = db.review_starts
cursor=collection.find({})
start_dates={}
for start in cursor:
    start_dates[start['_id']]=start['first_review']


#access review database

collection = db.reviews_rest
#limit only for processing time during testing - remove before final run
cursor=collection.find({})#.limit()
reviews=[]
for rev in cursor:
    reviews.append(rev)

# sort reviews by date + business for cumulative calculation
reviews.sort(key=lambda x: x['business_id']+x['date'])

#calculate averages first and store as "matrix"
#review averages actually counts in this module
review_averages=[]
last_id=""
x=0

for idx,review in enumerate(reviews):
    bus_id=review['business_id']
    if bus_id!=last_id:
        # tuple (id, cumulative review count, review date)
        review_averages.append([(review['business_id'],float(1),review['date'])])
        last_id=bus_id
        x+=1
    else:
        last_rec=review_averages[-1][-1]
        review_averages[-1].append((review['business_id'],last_rec[1]+float(1),review['date']))



# create monthly frequency from per review frequency
business_ratings={}
# tuple (id, cumulative stars, cumulative count, review stars, review date)
last_id=""
for idx,bus in enumerate(review_averages):
    bus_id=bus[0][0]
    business_ratings[bus_id]={}
    business_ratings[bus_id]['ratings']=[]
    start_date=datetime.datetime.strptime(bus[0][2], "%Y-%m-%d").date()
    end_date=datetime.datetime.strptime(bus[-1][2], "%Y-%m-%d").date()
    duration = (end_date-start_date).days
    #print start_date,end_date,duration
    #setup dates for record
    dates=[]
    x=start_date
    while x<end_date:
        x+=timedelta(days=30)
        dates.append(x)

    for p,date in enumerate(dates):
        for x,rev_avg in enumerate(bus):
            rdate=datetime.datetime.strptime(rev_avg[2], "%Y-%m-%d").date()
            #print rdate,date,rev_avg
            if rdate>date:
                business_ratings[bus_id]['ratings'].append((bus[x-1][1],date,p+1))
                break
#write to file count,age
thefile=open(dir+'counts_time.txt','w+')
minlength=6
for bus in business_ratings:
    for month in business_ratings[bus]['ratings']:
        if len(business_ratings[bus]['ratings'])>minlength:
            thefile.write(bus+','+str(month[0])+','+str(month[2])+'\n')
__author__ = 'davidgreenfield'
