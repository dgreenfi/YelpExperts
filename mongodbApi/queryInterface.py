from pymongo import MongoClient
import datetime


client = MongoClient('Karans-MacBook-Air.local')

db = client.yelp
collection = db.users
cursor = collection.find_one()
print cursor


collectionReviews = db.reviews
cursor = collectionReviews.distinct('business_id')

collectionSmallReviews = db.smallReviews
smallCursor = collectionSmallReviews.distinct('business_id')

print "Begin : ",datetime.datetime.now()
zeroReviews = 0
lessThan10 = 0
lessThan20 = 0
lessThan40 = 0
lessThan100 = 0
lessThan200 = 0
lessThan500 = 0
greaterThan500 = 0
count = 0
for c in cursor:
    #print count," ",c
    rec = collectionReviews.find( {"business_id" : c} ).count()
    print rec
    records = int(rec)
    if records == 0:
        zeroReviews += 1
    elif records > 0 and records < 10:
        lessThan10 += 1
    elif records > 10 and records < 20:
        lessThan20 += 1
    elif records > 20 and records < 40:
        lessThan40  += 1
    elif records > 40 and records < 100:
        lessThan100 += 1
    elif records > 100 and records < 200:
        lessThan200 += 1
    elif records > 200 and records < 500:
        lessThan500 += 1
    else:
        greaterThan500 += 1

    #print c," : ",records
    print " 0 reviews : ",zeroReviews
    print " < 10 ",lessThan10
    print " < 20 ",lessThan20
    print " < 40 ",lessThan40
    print " < 100 ",lessThan100
    print " < 200 ",lessThan200
    print " < 500 ",lessThan500
    print " > 500 ",greaterThan500


print " 0 reviews : ",zeroReviews
print " < 10 ",lessThan10
print " < 20 ",lessThan20
print " < 40 ",lessThan40
print " < 100 ",lessThan100
print " < 200 ",lessThan200
print " < 500 ",lessThan500
print " > 500 ",greaterThan500



print "End :",datetime.datetime.now()






__author__ = 'karanmatnani'
