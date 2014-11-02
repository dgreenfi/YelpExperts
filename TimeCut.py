import json
import datetime
from datetime import timedelta


rootdir='/Users/davidgreenfield/Downloads/yelp_dataset_challenge/'
review_file='yelp_academic_dataset_review.json'
#review_file='yelp_academic_dataset_review_sample.json'
review_data=[]

def time_cut():
    with open(rootdir+review_file) as f:
        for line in f:
            review_data.append(json.loads(line))


    min_date=datetime.date.today()
    max_date=datetime.datetime.strptime('1900-01-01', "%Y-%m-%d").date()

    for rev in review_data:
        #print rev['date']

        tempdate=datetime.datetime.strptime(rev['date'], "%Y-%m-%d").date()
        #print tempdate-min_date<timedelta(0)
        if tempdate<min_date:
            min_date=tempdate
        if tempdate>max_date:
            max_date=tempdate

    print min_date,max_date
if __name__ == '__main__':
    time_cut()

__author__ = 'davidgreenfield'
