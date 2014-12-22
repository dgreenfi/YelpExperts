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
    sizes=[5000,10000,20000]
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

####### Load accuracy experts
    datafile="/Users/davidgreenfield/socialfinalproject/mongodbApi/accuracy_Authorities.txt"
    experts_a=[]
    f=open(datafile,'r')
    experts_a= f.read().splitlines()
    experts_a= [x.split('\t')[0] for x in experts_a]
    experts_a=experts_a[0:expertsize]


    collection = db.reviews_rest
    cursor = collection.find()
    latlons=[]
    names=[]
    for review in cursor:
        bus_info= business[review['business_id']]
        bus_start=datetime.datetime.strptime(bus_info['first_review'], "%Y-%m-%d").date()
        rev_date=datetime.datetime.strptime(review['date'], "%Y-%m-%d").date()
        #print bus_start,rev_date
        if bus_start+timedelta(days=180)>rev_date:
            if rev_date<datetime.datetime.strptime("2014-01-01", "%Y-%m-%d").date():
                if rev_date>datetime.datetime.strptime("2013-01-01", "%Y-%m-%d").date():
                    if float(review['stars'])>3:
                        latlons.append((bus_info['latitude'],bus_info['longitude']))
                        names.append(str(bus_info['stars']))
######## output javascript

    with open('latlong_experts.txt','w') as op1:
        #op1.write("Authorities\n")
        for auth in latlons:

                op1.write("new google.maps.LatLng("+str(auth[0])+","+str(auth[1])+"),\n")

        for x,auth in enumerate(latlons):
                op1.write("var myLatlng"+str(x)+"=new google.maps.LatLng("+str(auth[0])+","+str(auth[1])+");\n")

                op1.write("var marker = new google.maps.Marker({\n")
                op1.write("position: myLatlng"+str(x)+",\n")
                op1.write("map: map,\n")
                op1.write("title: "+chr(39)+names[x]+chr(39)+"\n")
                op1.write("});\n")
        op1.close()
if __name__ == '__main__':
    main()

__author__ = 'davidgreenfield'
