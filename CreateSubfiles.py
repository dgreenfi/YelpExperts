import json
import csv

def create_subfiles():
    rootdir='/Users/dgreenfield/Downloads/yelp_dataset_challenge_academic_dataset_test/'
    business_file='yelp_academic_dataset_business.json'
    review_file='yelp_academic_dataset_review.json'

    categories=[]
    business_data = {}
    business_madison=[]
    #store business data in dictionary for merge w review data, could load to MySql if needed
    with open(rootdir+business_file) as f:
        for line in f:
            temp=json.loads(line)
            business_data[temp['business_id']]=line
            for category in temp['categories']:
                categories.append(category)
            if temp['city']=='Madison':
                business_madison.append(temp)

    #create category list
    save_data(list(set(categories)),rootdir+'yelp_categories.txt')
    save_data_json(business_madison,rootdir+'yelp_business_madison.json')
    review_data = []
    review_madison=[]
    review_madison_pizza=[]
    with open(rootdir+review_file) as f:
        for line in f:
            temp=json.loads(line)
            review_data.append(json.loads(line))
            temp_b=json.loads( business_data[temp['business_id']])
            if temp_b['city']=='Madison':
                review_madison.append(line)

    save_data_json(review_madison,rootdir+'yelp_review_madison.json')

def save_data(list,outfile):
   with open(outfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in list:
            writer.writerow([item])

def save_data_json(list,outfile):
   with open(outfile, 'wb') as file:
        json.dump(list,file)

if __name__ == '__main__':
    create_subfiles()

__author__ = 'dgreenfield'
