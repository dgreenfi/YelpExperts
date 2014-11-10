from pymongo import MongoClient
from bson.son import SON
client = MongoClient('Davids-MacBook-Air.local')

#db = client.test
#collection = db.testreviews
# Print a list of collections



#cursor=collection.aggregate([{"$sort": { "business_id": 1, "date": 1 }} ,{"$group": {"_id": "$business_id", "firstRev":{ "$first": "$date" }}}])
#firstdates=cursor['result']
#for start in firstdates:
#    print start

#cursor = collection.find().limit(100)
#for doc in cursor:
#    print(doc['business_id'],doc['date'])

#full file
db = client.yelp
collection = db.reviews
cursor = collection.find_one()
print cursor

cursor=collection.aggregate([{"$sort": { "business_id": 1, "date": 1 }} ,{"$group": {"_id": "$business_id", "firstRev":{ "$first": "$date" }}}],allowDiskUse=True)
firstdates=cursor['result']
for start in firstdates:
    print start



__author__ = 'davidgreenfield'
