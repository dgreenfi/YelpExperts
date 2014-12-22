__author__ = 'davidgreenfield'

from pymongo import MongoClient
import networkx as nx
import datetime
import operator
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from scipy import stats

def main():
    sizes=[10,50,100,200,300,400,500,1000,2000,5000,10000,20000]
    for size in sizes:
        calc(size)



def calc(expertsize):
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


####### Load baseline experts
    datafile="/Users/davidgreenfield/socialfinalproject/mongodbApi/baseline_Authorities.txt"
    experts_b=[]
    f=open(datafile,'r')
    experts_b= f.read().splitlines()
    experts_b= [x.split('\t')[0] for x in experts_b]
    experts_b=experts_b[0:expertsize]

####### Load accuracy experts
    datafile="/Users/davidgreenfield/socialfinalproject/mongodbApi/accuracy_Authorities.txt"
    experts_a=[]
    f=open(datafile,'r')
    experts_a= f.read().splitlines()
    experts_a= [x.split('\t')[0] for x in experts_a]
    experts_a=experts_a[0:expertsize]


######## Core Results  ###########

#variance of expert ratings vs consensus

#variance of yelp ratings vs consensus


#variance of overall ratings vs consensus
    collection = db.reviews_rest
    cursor = collection.find()
    #difference between prediction and consensus
    diffs=[]
    diffs_e=[]
    diffs_ex_b=[]
    diffs_ex_a=[]
    diffs_perf=[]
    ests=[]
    actual=[]
    ests_e=[]
    actual_e=[]
    actual_a=[]
    ests_ex_b=[]
    ests_ex_a=[]
    actual_ex_b=[]
    actual_ex_a=[]
    #score review id the
    for review in cursor:
       # print review
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        #print bus_start,rev_date

        if bus_start+timedelta(days=180)>rev_date:
            if rev_date<datetime.datetime.strptime("2014-01-01", "%Y-%m-%d").date():
                if rev_date>datetime.datetime.strptime("2013-01-01", "%Y-%m-%d").date():
                    if bus_info['review_count']>20:
                #need threshold for business age now
                        diff=abs(float(review['stars'])-float(bus_info['avg_stars_calc']))
                        diffs.append(diff)
                        rem=float(bus_info['avg_stars_calc'])%1
                        if rem>.5:
                            diffs_perf.append(1-rem)
                        else:
                            diffs_perf.append(rem)
                        ests.append(float(review['stars']))
                        actual.append(float(bus_info['avg_stars_calc']))
                        user_id=review['user_id']
                        if user_id in elite_ids:
                            diffs_e.append(diff)
                            ests_e.append(float(review['stars']))
                            actual_e.append(float(bus_info['avg_stars_calc']))
                        if user_id in experts_b:
                            diffs_ex_b.append(diff)
                            ests_ex_b.append(float(review['stars']))
                            actual_ex_b.append(float(bus_info['avg_stars_calc']))
                        if user_id in experts_a:
                            diffs_ex_a.append(diff)
                            ests_ex_a.append(float(review['stars']))
                            actual_ex_a.append(float(bus_info['avg_stars_calc']))

            #print diff
            #print review['stars'],bus_info['stars'],bus_info['avg_stars_calc']
    # print "# of reviews in incubation period"
    # print len(diffs)
    # print "Standard Deviation of General Population Reviews from Consensus:"
    # print np.std(diffs)
    # print "Variance of General Population Reviews from Consensus:"
    # print np.var(diffs)
    # print "MSE of General Elite Reviews from Consensus:"
    # print mse_from_errors(diffs)
    # #elite diffs
    # print "# of reviews in incubation period- Elite"
    # print len(diffs_e)
    # print "Standard Deviation of Elite Reviews from Consensus:"
    # print np.std(diffs_e)
    # print "Variance of General Elite Reviews from Consensus:"
    # print np.var(diffs_e)
    # print "MSE of General Elite Reviews from Consensus:"
    # print mse_from_errors(diffs_e)

    #   #expert diffs
    # print "# of reviews in incubation period- Expert"
    # print len(diffs_ex_b)
    # print "Standard Deviation of Expert Reviews from Consensus:"
    # print np.std(diffs_ex_b)
    # print "Variance of General Expert Reviews from Consensus:"
    # print np.var(diffs_ex_b)
    # print "MSE of General Elite Reviews from Consensus:"
    # print mse_from_errors(diffs_ex_b)
    #
    # print "ANOVA"
    # print stats.f_oneway(diffs,diffs_e,diffs_ex_b)
    print "Tests for Expert Group Size"+ str(expertsize)
    print "T-Test Elites"
    print stats.ttest_ind(diffs,diffs_e)

    print "T-Test Experts"
    print stats.ttest_ind(diffs,diffs_ex_b)

    print "T-Test Elite vs Baseline Experts"
    print stats.ttest_ind(diffs_e,diffs_ex_b)

    print "T-Test Elite vs Accuracy Experts"
    print stats.ttest_ind(diffs_e,diffs_ex_a)
    print "T-Test Baseline vs Accuracy Experts"
    print stats.ttest_ind(diffs_ex_b,diffs_ex_a)
    print "Mean Error Population, Elite, Expert"
    print np.mean(diffs)
    print "Count: " + str(len(diffs))
    print np.mean(diffs_e)
    print "Count: " + str(len(diffs_e))
    print np.mean(diffs_ex_b)
    print "Count: " + str(len(diffs_ex_b))
    print np.mean(diffs_ex_a)
    print "Count: " + str(len(diffs_ex_a))
    print np.mean(diffs_perf)
    print "Count: " + str(len(diffs_perf))
    print "Machine Stats (N experts,mean population,mean elite,mean base experts, mean acc experts,review count pop,review count elite, review count baseline, review count accuracy)"
    print expertsize,np.mean(diffs),np.mean(diffs_e),np.mean(diffs_ex_b),np.mean(diffs_ex_a),len(diffs),len(diffs_e),len(diffs_ex_b),len(diffs_ex_a)
    print "Baseline HITS Top "+str(expertsize)+" & "+str(np.mean(diffs_ex_b)/4*100) +" & "+str(len(diffs_ex_b)) +"\\"
    print "Weighted HITS Top "+str(expertsize)+" & "+str(np.mean(diffs_ex_a)/4*100) +" & "+str(len(diffs_ex_a)) +"\\\\hline"
    #quit()
######## Interesting Stats  ############
    plots=0
    if plots==1:
        db = client.yelp
        collection = db.user
    # Average Review rating experts
        stars_ex_b=[]
        for expert in experts_b:
            cursor = collection.find({"user_id":expert})
            for x in cursor:
                stars_ex_b.append(x['average_stars'])

        print "Average Expert Rating:"
        print np.mean(stars_ex_b),np.std(stars_ex_b)
        print "User Count:"
        print len(stars_ex_b)

    # Distribution of overall population users
        font = {'family' : 'serif',
            'color'  : 'darkred',
            'weight' : 'normal',
            'size'   : 12,
            }
        plt.hist(stars_ex_b, bins=40)
        plt.title('Average User Rating Histogram - Baseline Experts (N='+str(expertsize)+')')
        plt.xlabel('Age User Rating')
        plt.ylabel('Number of Users')
        plt.show()

    # Average Review rating Acc_experts
        stars_ex_a=[]
        for expert in experts_a:
            cursor = collection.find({"user_id":expert})
            for x in cursor:
                stars_ex_a.append(x['average_stars'])

        print "Average Expert Rating:"
        print np.mean(stars_ex_a),np.std(stars_ex_a)
        print "User Count:"
        print len(stars_ex_a)

    # Distribution of accuracy experts users

        plt.hist(stars_ex_a, bins=40)
        plt.title('Average User Rating Histogram - Accuracy Weighted (N='+str(expertsize)+')')
        plt.xlabel('Age User Rating')
        plt.ylabel('Number of Users')
        plt.show()

    # Average Review rating yelp elite
        cursor = collection.find().where("if (this.elite.length > 0){return this;}")
        stars_e=[x['average_stars'] for x in cursor]
        print "Average Elite Rating:"
        print np.mean(stars_e),np.std(stars_e)
        print "User Count:"
        print len(stars_e)

    # Distribution of yelp elite

        plt.hist(stars_e, bins=40)
        plt.title('Average User Rating Histogram - Elite Only')
        plt.xlabel('Age User Rating')
        plt.ylabel('Number of Users')
        plt.show()

    # Average Review rating overall population without elite
        cursor = collection.find({"review_count":{"$gt":10}}).where("if (this.elite.length <1){return this;}")
        stars_o=[x['average_stars'] for x in cursor]

        print "Average Population Rating Excluding Elite (>10 Reviews):"
        print np.mean(stars_o),np.std(stars_o)
        print "User Count:"
        print len(stars_o)

    # Distribution of overall population users
        plt.title('Average User Rating Histogram - Non-Elite Population (>10 Reviews)')
        plt.xlabel('Age User Rating')
        plt.ylabel('Number of Users')
        plt.hist(stars_o, bins=40)
        plt.show()

def mse_from_errors(error_list):
    sq_errors=[float(x**x) for x in error_list]
    n = float(len(sq_errors))
    return np.mean(sq_errors)/n

def variance(list):
    pass


if __name__ == '__main__':
    main()
