import networkx
import csv
import json
from operator import itemgetter
from collections import defaultdict

def load_graph():
    rootdir='/Users/dgreenfield/Downloads/yelp_dataset_challenge_academic_dataset_test/'
    review_file='yelp_review_madison.json'
    business_file='yelp_business_madison.json'
    rankfile='yelp_business_madison_exrank.csv'

    with open(rootdir+business_file) as file:
        business=json.load(file)

    with open(rootdir+review_file) as rfile:
        review=json.load(rfile)

    G = networkx.DiGraph()
    for line in review:
        temp=json.loads(line)
        G.add_edge(temp['user_id']+'-U',temp['business_id']+'-B')
        if temp['votes']['useful']>2:
            G.add_edge(temp['business_id']+'-B',temp['user_id']+'-U')

    business_dict={}
    for line in business:
        business_dict[line['business_id']+'-B']=line

    print G.number_of_nodes()
    head= G.nodes()[0:10]
    all_nodes=G.nodes()
    ranks=networkx.pagerank(G,alpha=.85,max_iter=150)

    ### compile new yelp rank
    user_ranks=[]
    business_ranks=[]
    for node in all_nodes:
        if node[-2:]=='-U':
            user_ranks.append((node,ranks[node]))
        if node[-2:]=='-B':
            business_ranks.append((node,ranks[node]))

    user_ranks=sorted(user_ranks,key=itemgetter(1),reverse=True)
    business_ranks=sorted(business_ranks,key=itemgetter(1),reverse=True)
    print user_ranks[0:100]
    for bus in business_ranks[0:10]:
        print business_dict[bus[0]]['name']

    ranks=compute_expert_rank(user_ranks[0:200],business_dict,review)
    output_ranks(ranks,rankfile)

def compute_expert_rank(ranks,business_dict,reviews):
    #recompute ratings using
    expert_ranks=[]
    expertlist=[x for (x,y) in ranks]
    ratings_by_loc={}
    for review in reviews:
        rev=json.loads(review)
        #print rev['business_id']
        if rev['business_id'] not in ratings_by_loc.keys():
            ratings_by_loc[rev['business_id']]={}
        if rev['user_id']+'-U' in expertlist:
            try:
                ratings_by_loc[rev['business_id']]['expert_ratings'].append(rev['stars'])
            except:
                ratings_by_loc[rev['business_id']].setdefault('expert_ratings',[]).append(rev['stars'])
        else:
            try:
                ratings_by_loc[rev['business_id']]['non_expert_ratings'].append(rev['stars'])
            except:
                ratings_by_loc[rev['business_id']].setdefault('non_expert_ratings',[]).append(rev['stars'])
        try:
                ratings_by_loc[rev['business_id']]['all_ratings'].append(rev['stars'])
        except:
                ratings_by_loc[rev['business_id']].setdefault('all_ratings',[]).append(rev['stars'])
    output=[]
    for loc in ratings_by_loc:
        outline=[business_dict[loc+'-B']['name']]
        print ratings_by_loc[loc],loc
        for k in ratings_by_loc[loc].keys():
            print mean(ratings_by_loc[loc][k]),k
            outline.append((mean(ratings_by_loc[loc][k]),k,len((ratings_by_loc[loc][k]))))
        if 'expert_ratings' in ratings_by_loc[loc].keys():
            outline.append(('expert_ratio',float(len(ratings_by_loc[loc]['expert_ratings']))/float(len((ratings_by_loc[loc]['all_ratings'])))))
        # temp for browsing
        if len(ratings_by_loc[loc]['all_ratings'])>20:
            if 'expert_ratings' in ratings_by_loc[loc].keys():
                if mean(ratings_by_loc[loc]['expert_ratings'])>4.5:
                    output.append(outline)
    return output
       # print mean(ratings_by_loc[loc['expert_ratings']]),mean(ratings_by_loc[loc['non_expert_ratings']]),mean(ratings_by_loc[loc['all_ratings']])

def output_ranks(lines,filename):
    with open(filename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for line in lines:
            spamwriter.writerow([line])

def mean(l):
    l=[float(x) for x in l]
    try:
        return reduce(lambda x, y: x + y, l) / len(l)
    except TypeError:
        return 0

if __name__ == '__main__':
    load_graph()
__author__ = 'dgreenfield'
