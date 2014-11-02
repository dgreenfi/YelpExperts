import networkx
import json
import csv


def create_edges():
    rootdir='/Users/davidgreenfield/Downloads/yelp_dataset_challenge_academic_dataset_test/'
    business_file='yelp_academic_dataset_business.json'
    review_file='yelp_academic_dataset_review.json'
    #review_file='review_sample.json'
    outfile='yelp_academic_dataset_edges.csv'

    #json_data=open(rootdir+business_file)
    business_data = {}
    with open(rootdir+business_file) as f:
        for line in f:
            temp=json.loads(line)
            business_data[temp['business_id']]=line

    review_data = []
    with open(rootdir+review_file) as f:
        for line in f:
            review_data.append(json.loads(line))

    print review_data[0:10]
    edges=[]
    for review in review_data:
        temp= json.loads(business_data[review['business_id']])
        if temp['city'].lower()=='madison'.lower():

            # create an edge from the user to location - always
            edges.append((review['user_id']+'-U',review['business_id']+'-B'))

            #create an edge from location if at least 5 people find the review useful
            if review['votes']['useful']>5:
                edges.append((review['business_id']+'-B',review['user_id']+'-U'))

    edges=list(set(edges))
    output_edges(edges,rootdir+outfile)

def output_edges(edgelist,filename):
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for edge in edgelist:
            spamwriter.writerow([edge[0],edge[1]])

if __name__ == '__main__':
    create_edges()






__author__ = 'dgreenfield'
