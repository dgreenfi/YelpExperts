import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#hw example w 1 weights
A= np.matrix('0 0 1 1 1 0;0 0 0 0 1 1;1 0 0 0 0 0;1 0 0 0 0 0;1 1 0 0 0 0;0 1 0 0 0 0')
u= np.matrix('1;1;1;1;1;1')
v=A.transpose().dot(u)
u=A.dot(v)
print u,v
v=A.transpose().dot(u)
u=A.dot(v)
print u,v
v=A.transpose().dot(u)
u=A.dot(v)
print u

G=nx.from_numpy_matrix(A)

label={0:"A",1:"B",2:"C",3:"X",4:"Y",5:"Z"}
nx.draw(G,pos=nx.spring_layout(G))
plt.axis('off')
plt.savefig("labels_and_colors.png") # save as png
plt.show()

plt.draw()
#plt.show()

#hw example w non 1 weights
A= np.matrix('0 0 .25 .25 1 0;0 0 0 0 1 1;.25 0 0 0 0 0;.25 0 0 0 0 0;1 1 0 0 0 0;0 1 0 0 0 0')
u= np.matrix('1;1;1;1;1;1')
v=A.transpose().dot(u)
u=A.dot(v)
print u
v=A.transpose().dot(u)
u=A.dot(v)
print u
v=A.transpose().dot(u)
u=A.dot(v)
print u


G=nx.from_numpy_matrix(A)
nx.draw(G)
plt.draw()
#plt.show()


edgelist=[(1,3),(1,4),(1,5),(1,3)]


__author__ = 'davidgreenfield'
