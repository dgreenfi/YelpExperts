import numpy as np
from collections import Counter as c
import matplotlib.pyplot as plt
from itertools import groupby

datafile='/Users/davidgreenfield/socialfinalproject/rev_ages.txt'
f=open(datafile,'r')
ages= f.read().splitlines()

ages=[float(x) for x in ages]

datafile='/Users/davidgreenfield/socialfinalproject/rev_ratings.txt'
f=open(datafile,'r')
ratings= f.read().splitlines()
ratings=[float(x) for x in ratings]

datafile='/Users/davidgreenfield/socialfinalproject/variance_time.txt'
f=open(datafile,'r')
variances= f.read().splitlines()
variances=[float(x) for x in variances]

agerate=zip(ages,ratings)
agerate=sorted(agerate,key=lambda x: x[0])

stats=[]
for key, rows in groupby(agerate,lambda x: x[0]):
    stats.append((key, sum(r[1] for r in rows)))

finstats=[]
x=c(ages)
for age in stats:
    finstats.append((age[1]/x[age[0]]))

print finstats[0:10]

h=np.histogram(ages,bins=200)
print h
plt.scatter(range(0,len(finstats)),finstats)
plt.xlabel('Age after 1st Review')
plt.ylabel('Average Rating')
plt.ylim(1,5)
plt.title('Average Rating by Age')
plt.show()

plt.plot(variances)
plt.show()

print xchange_stats[week]
cnts=[x[y] for y in x]
plt.scatter(range(1,len(cnts)),cnts[1:len(cnts)])
plt.xlabel('Age after 1st Review')
plt.ylabel('Count of Reviews')
plt.ylim(-500,2000)
plt.title('Age vs Quantity of Reviews (Restaurants Only)')
plt.show()

def age_ave(data):
    df = pd.DataFrame(data)
    grouped = df.groupby(['age'])
    sum = grouped.mean()
    return [{'age': r} for r, kv in sum.iterrows()]


__author__ = 'davidgreenfield'
