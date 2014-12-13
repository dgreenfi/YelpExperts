__author__ = 'davidgreenfield'

from pymongo import MongoClient
import networkx as nx
import datetime
import operator
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta


def main():
    client = MongoClient('Davids-MacBook-Air.local')
    db = client.yelp
    collection = db.reviews_rest

####### Load Business lookup #####
    business={}
    collection = db.business
    cursor = collection.find({"avg_stars_calc":{"$gt":0}})
    for bus in cursor:
        business[bus['business_id']]=bus

####### Load Elite Users  ############
    collection = db.user
    cursor = collection.find().where("if (this.elite.length > 0){return this;}")
    elite_ids=[u['user_id'] for u in cursor]


######## Core Results  ###########

#variance of expert ratings vs consensus

#variance of yelp ratings vs consensus


#variance of overall ratings vs consensus
    collection = db.reviews_rest
    cursor = collection.find()
    #difference between prediction and consensus
    diffs=[]
    diffs_e=[]
    #score review id the
    for review in cursor:
       # print review
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        print bus_start,rev_date

        if bus_start+timedelta(days=150)>rev_date:
            #need threshold for business age now
            diff=abs(float(review['stars'])-float(bus_info['avg_stars_calc']))
            diffs.append(diff)
            user_id=review['user_id']
            if user_id in elite_ids:
                diffs_e.append(diff)
            print diff
            print review['stars'],bus_info['stars'],bus_info['avg_stars_calc']
    print "# of reviews in incubation period"
    print len(diffs)
    print "Standard Deviation of General Population Reviews from Consensus:"
    print np.std(diffs)
    print "Variance of General Population Reviews from Consensus:"
    print np.var(diffs)
    #elite diffs
    print "# of reviews in incubation period- Elite"
    print len(diffs_e)
    print "Standard Deviation of Elite Reviews from Consensus:"
    print np.std(diffs_e)
    print "Variance of General Elite Reviews from Consensus:"
    print np.var(diffs_e)
    quit()


######## Interesting Stats  ############

    db = client.yelp
    collection = db.user
# Average Review rating experts

# Average Review rating yelp elite
    cursor = collection.find().where("if (this.elite.length > 0){return this;}")
    stars_e=[x['average_stars'] for x in cursor]
    print "Average Elite Rating:"
    print np.mean(stars_e)
    print "User Count:"
    print len(stars_e)

# Distribution of overall population users

    plt.hist(stars_e, bins=40)
    plt.title('Average User Rating Historgram - Elite Only')
    plt.xlabel('Age User Rating')
    plt.ylabel('Number of Users')
    plt.show()

# Average Review rating overall population
    cursor = collection.find({"review_count":{"$gt":10}})
    stars_o=[x['average_stars'] for x in cursor]

    print "Average Population Rating (>10 Reviews):"
    print np.mean(stars_o)
    print "User Count:"
    print len(stars_o)

# Distribution of overall population users
    plt.title('Average User Rating Historgram - Total Population')
    plt.xlabel('Age User Rating')
    plt.ylabel('Number of Users')
    plt.hist(stars_o, bins=40)
    plt.show()
if __name__ == '__main__':
    main()

def variance(list):
    pass


