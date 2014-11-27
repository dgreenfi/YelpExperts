from pymongo import MongoClient
client = MongoClient('Davids-MacBook-Air.local')
db = client.yelp

#access review database
collection = db.reviews
#query for first date for each business id
cursor=collection.aggregate([{"$sort": { "business_id": 1, "date": 1 }} ,{"$group": {"_id": "$business_id", "first_review":{ "$first": "$date" }}}],allowDiskUse=True)
firstdates=cursor['result']



collection=db.review_starts
for start in firstdates:
    #print start['_id'] in biz_list
    collection.insert(start)


__author__ = 'davidgreenfield'


# create histograms:
# run CreateReviewStarts
# run DataStats
# run histogram