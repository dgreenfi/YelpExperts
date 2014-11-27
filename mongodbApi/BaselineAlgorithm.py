from pymongo import MongoClient
import networkx as nx
import datetime
import operator

client = MongoClient('Karans-MacBook-Air.local')

print "Begin",datetime.datetime.now()
db = client.yelp
collection = db.reviews_rest

cursor = collection.find()              # This will hold all the reviews for restaurants

user_rest = nx.DiGraph()

for review in cursor:
    restId = str(review['business_id'])
    userId = str(review['user_id'])

    user_rest.add_edge(userId, restId)


print user_rest.number_of_nodes()

hubs = {}
authorities = {}

#hubs,authorities = nx.hits(user_rest,max_iter=10, tol=1.0e-8, nstart=0,normalized=True)
hubs,authorities = nx.hits(user_rest,max_iter=1000, tol = 1.0e-3,normalized=False)

print "End of HITS",datetime.datetime.now()

sorted_hubs = sorted(hubs.items(), key=operator.itemgetter(1), reverse=True)
print sorted_hubs

with open('baseline_Hubs.txt','w') as op:
    op.write("Hubs")
    for hub in sorted_hubs:
        if hub[1] > 0:       # When v ==0, we actually have an authority here
            op.write(hub[0]+" : "+str(hub[1])+"\n")
    op.close()

sorted_auths = sorted(hubs.items(), key=operator.itemgetter(1), reverse=True)
print "Sorted auths length : ",len(sorted_auths)
with open('baseline_Authorities.txt','w') as op1:
    op1.write("Authorities")
    for auth in sorted_auths:
        if auth[1]>0:         # When v ==0, we actually have a hub here
            op1.write(auth[0]+" : "+str(auth[1])+"\n")
    op1.close()





'''
    Gets the accuracy of our prediction.
    1. Get the list of our experts: the top n% of authorities
    2. Get the list of users from the users in mongodb
    3. Generate the accuracy by calculating True positives,
'''
def get_Accuracy():

    TP = 0
    FP = 0
    #Derived_Experts = sorted_auths[1:int((0.1*len(sorted_auths)))][0]
    Derived_Experts = sorted_auths[0:100]
    Derived_Experts =[x[0] for x in Derived_Experts]

    print Derived_Experts.__len__()
    db = client.yelp
    collection = db.users

    cursor = collection.find().where("if (this.elite.length > 0){return this;}")              # This will hold all elite users

    YelpExperts = []

    for user in cursor:
        YelpExperts.append(user['user_id'])

    print "Yelp has ",YelpExperts.__len__()," experts"
    for dExpert in Derived_Experts:
        if dExpert in YelpExperts:
            TP += 1
        else:
            FP += 1

    print "True positives:",TP
    print "False positives:",FP
    print "Total : ",TP+FP

get_Accuracy()
__author__ = 'karanmatnani'
