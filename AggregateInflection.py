import numpy as np
import matplotlib.pyplot as plt
datafile='counts_time.txt'
f=open(datafile,'r')
counts= f.read().splitlines()
counts= [x.split(',') for x in counts]

#dictionary of counts by age 3:[1,4,5,6] to take avg of
minlength=18
agecount={}
for count in counts:
    if count[2] not in agecount.keys():
        agecount[count[2]]=[float(count[1])]
    else:
        agecount[count[2]].append(float(count[1]))
avgcount=[]
for count in agecount:
    avgcount.append((int(count),np.mean(agecount[count])))

avgcount.sort(key=lambda x: x[0])
ages=[int(x[0]) for x in avgcount]
fincounts=[x[1] for x in avgcount]



plt.plot(ages,fincounts)
plt.xlabel('Age of restaurant')
plt.ylabel('Avg Count of Reviews')
plt.title('Age vs Quantity of Reviews (Restaurants Only)')
plt.show()


plt.plot(ages[0:24],fincounts[0:24])
plt.xlabel('Age of restaurant')
plt.ylabel('Avg Count of Reviews')
plt.title('Age vs Quantity of Reviews (Restaurants Only)')
plt.show()
#chart results



__author__ = 'davidgreenfield'
