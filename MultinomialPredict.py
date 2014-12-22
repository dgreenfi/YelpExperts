from pymongo import MongoClient
import networkx as nx
import datetime
import operator
from datetime import timedelta
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
import numpy as np


client = MongoClient('Davids-MacBook-Air.local')
print "Begin",datetime.datetime.now()
def main():
    db = client.yelp


    ####### Load Business lookup #####
    business={}
    collection = db.business
    cursor = collection.find({"avg_stars_calc":{"$gt":0}})
    for bus in cursor:
        business[bus['business_id']]=bus

    ####### Load User lookup #####
    users={}
    collection = db.user
    cursor = collection.find()
    for user in cursor:
        users[user['user_id']]=user


    ####### Calc accuracy training period
    acc_dict={}
    y=[]
    collection = db.reviews_rest
    cursor = collection.find() .limit(1000)             # This will hold all the reviews for restaurants
    for review in cursor:
        restId = str(review['business_id'])
        userId = str(review['user_id'])
        try:
            userlist = users[review['user_id']]['review_ratings']
            conslist = users[review['user_id']]['rest_ratings']
        except:
            userlist =[]
            conslist=[]
        user_acc= user_Accuracy(userlist,conslist)
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        if bus_start+timedelta(days=180)>rev_date:
                if bus_start<datetime.datetime.strptime("2013-01-01", "%Y-%m-%d").date():
                    acc_dict[review['user_id']]=int(user_acc*100)



    print acc_dict
    ############ setup feature matrix
    X=np.zeros((len(acc_dict.keys()),10))

    y=np.zeros(len(acc_dict.keys()))
    num=0
    for user in users:
        if user in acc_dict.keys():
            feat=[]
            feat.append(users[user]['average_stars'])
            year_joined=int(users[user]['yelping_since'][0:4])
            feat.append(year_joined)
            feat.append(len(users[user]['friends']))
            feat.append(users[user]['fans'])
            feat.append(users[user]['votes']['useful'])
            feat.append(users[user]['votes']['funny'])
            feat.append(users[user]['votes']['cool'])
            feat.append(users[user]['review_count'])
            try:
                feat.append(users[user]['compliments']['plain'])
            except:
                feat.append(0)
            feat.append(len(users[user]['elite']))
            print feat
            feat=np.asarray(feat)
            X[num]=feat
            y[num]=acc_dict[user]
            num+=1

    #print X,y

    ##### fit model
    clf = MultinomialNB()
    clf.fit(X, y)

    ##### assemble test set X
    collection = db.reviews_rest
    cursor = collection.find()            # This will hold all the reviews for restaurants
    test_user=[]
    for review in cursor:
       # print review
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        #print bus_start,rev_date
        if review["user_id"] not in test_user:
            test_user.append(review['user_id'])



    print test_user
    X_t=np.zeros((len(test_user),10))
    num=0
    y_names=[]
    for user in test_user:
        if user in acc_dict.keys():
            feat=[]
            feat.append(users[user]['average_stars'])
            year_joined=int(users[user]['yelping_since'][0:4])
            feat.append(year_joined)
            feat.append(len(users[user]['friends']))
            feat.append(users[user]['fans'])
            feat.append(users[user]['votes']['useful'])
            feat.append(users[user]['votes']['funny'])
            feat.append(users[user]['votes']['cool'])
            feat.append(users[user]['review_count'])
            try:
                feat.append(users[user]['compliments']['plain'])
            except:
                feat.append(0)
            feat.append(len(users[user]['elite']))
            print feat
            feat=np.asarray(feat)
            X_t[num]=feat
            y_names.append(user)
            num+=1
    #### predict from test data
    y_t=clf.predict(X_t)

    y_t_list=np.ndarray.tolist(y_t)
    acc_id = zip(y_names,y_t_list)
    sorted(acc_id, key=lambda x: x[1])
    ##### output experts
    with open('multinomial_Authorities.txt','w') as op1:
        #op1.write("Authorities\n")
        for auth in acc_id:
                  # When v ==0, we actually have a hub here
            op1.write(auth[0]+"\t"+str(auth[1])+"\n")
        op1.close()

def user_Accuracy(user_list,cons_list):

    diffs=[abs(b_i - a_i) for a_i, b_i in zip(user_list, cons_list)]
    diffs_sum=sum(diffs)
    try:
        acc=1-(diffs_sum/(4*float(len(diffs))))
    except:
        acc=0
    return acc

def acc_to_percentile(d):
    raw=[(key,d[key]) for key in d]


if __name__ == '__main__':
    main()


__author__ = 'davidgreenfield'
