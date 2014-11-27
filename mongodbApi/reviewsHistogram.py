import matplotlib.pyplot as plt

from numpy.random import normal
gaussian_numbers = [2495,631,431,334,108,25,184]
#plt.hist(gaussian_numbers, bins = (0,10,20,40,100,200,500,1000))
plt.plot([0,10,20,40,100,200,500,600],[0,3003,771,494,395,121,26,217],linewidth=4.0,color="red")
plt.title("Business Reviews Graph")
plt.xlabel("No. of reviews")
plt.ylabel("No. of Businesses")
plt.show()





__author__ = 'karanmatnani'