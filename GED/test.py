import networkx as nx
from matplotlib import pylab as pl

G = nx.karate_club_graph()
res = [0,1,2,3,4,5, 'parrot'] #I've added 'parrot', a node that's not in G
                              #just to demonstrate that G.subgraph is okay
                              #with nodes not in G.
pos = nx.spring_layout(G)  #setting the positions with respect to G, not k.
k = G.subgraph(res)

pl.figure()
nx.draw_networkx(k, pos=pos)

othersubgraph = G.subgraph(range(6,G.order()))
nx.draw_networkx(othersubgraph, pos=pos, node_color = 'b')
pl.show()