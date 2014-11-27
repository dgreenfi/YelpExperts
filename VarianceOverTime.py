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
cursor=collection.find({}).limit(50000)
reviews=[]
for rev in cursor:
    reviews.append(rev)

#sort by business id
reviews.sort(key=lambda x: x['business_id']+x['date'])
last_id=""
#calculate averages first and store as "matrix"
review_averages=[]
last_id=""
x=0
for idx,review in enumerate(reviews):
    bus_id=review['business_id']
    if bus_id!=last_id:
        # tuple (id, cumulative stars, cumulative count, review stars, review date)
        review_averages.append([(review['business_id'],float(review['stars']),float(1),float(review['stars']),review['date'])])
        last_id=bus_id
        x+=1
    else:
        last_rec=review_averages[-1][-1]
        #print last_rec[-1]
        newave=((last_rec[1]*last_rec[2])+float(review['stars']))/(last_rec[2]+float(1))
        review_averages[-1].append((review['business_id'],newave,last_rec[2]+float(1),float(review['stars']),review['date']))

# result is a list with all tuples for each id [[(id1),(id1)][(id2),(id2)]]
#for rev in review_averages:
 #   for x in rev:
  #      pass
        #print x

business_ratings={}
# tuple (id, cumulative stars, cumulative count, review stars, review date)
last_id=""
for idx,bus in enumerate(review_averages):
    bus_id=bus[0][0]
    business_ratings[bus_id]={}
    business_ratings[bus_id]['ratings']=[]
    start_date=datetime.datetime.strptime(bus[0][4], "%Y-%m-%d").date()
    end_date=datetime.datetime.strptime(bus[-1][4], "%Y-%m-%d").date()
    duration = (end_date-start_date).days
    #print start_date,end_date,duration
    #setup dates for record
    dates=[]
    x=start_date
    while x<end_date:
        x+=timedelta(days=30)
        dates.append(x)

    for date in dates:
        for x,rev_avg in enumerate(bus):
            rdate=datetime.datetime.strptime(rev_avg[4], "%Y-%m-%d").date()
            #print rdate,date,rev_avg
            if rdate>date:
                business_ratings[bus_id]['ratings'].append((bus[x-1][3],date))
                break


#create weekly/monthly changes

weekly_changes=[]
for bus in business_ratings:
    ratings=business_ratings[bus]['ratings']

    changes=[]
    for idx,rating in enumerate(ratings):
        #print rating[0],ratings[idx-1][0],rating[0]-ratings[idx-1][0],idx
        if idx>0:
            changes.append(abs(rating[0]-ratings[idx-1][0]))

    weekly_changes.append(changes)


#print business_ratings

print weekly_changes
print len(weekly_changes[0]),len(weekly_changes[1])
print len(weekly_changes)

change_stats={}
for bus in weekly_changes:
    for wk,chg in enumerate(bus):
        if wk not in change_stats.keys():
            change_stats[wk]=[]
        else:
            change_stats[wk].append(chg)

means=[]
for week in change_stats:
    print week
    means.append(np.mean(change_stats[week]))
    print len(change_stats[week])
print means



#for i in change_mat.transpose():
   # print i



thefile=open(dir+'variance_time.txt','w+')
for item in means:
  thefile.write("%s\n" % item)




        #check if last review



    #print review['business_id'],review['stars'],review['date']










__author__ = 'davidgreenfield'
