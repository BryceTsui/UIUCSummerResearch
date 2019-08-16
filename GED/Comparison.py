"""
This program is used to compare two different ways of edit distance.
You can ignore this program
"""

import networkx as nx

G1 = nx.DiGraph()
G1.add_node(1,label="1")
G1.add_node(2,label="2")

G1.add_edge(1,2)


G2 = nx.DiGraph()
G2.add_node(1,label="1")
G2.add_node(3,label="3")
G2.add_node(2)
G2.add_node(4)
G2.add_edge(1,2)





# G2.add_node(3,label="key")
nx.drawing.nx_pydot.write_dot(G2,"generate_G2.dot")

# def compare_node(a,b):
#     return a['label']==b['label']
#
# def compare_edge(e1,e2):
#     print("edge info")
#     print(e1)
#     return False
print('start')
for dis in nx.algorithms.similarity.optimize_graph_edit_distance(G1, G2,node_match=lambda a,b:True):#params contain edge_match,but it has considered the edge but ignore the attributes in edges, in our project we can ignore the attributes in edges
    print(dis)

print('end')



import gmatch4py as gm
#ged=gm.GraphEditDistance(1,1,1,1) # node del node ins edge del edge in
HED = gm.HED(1,1,1,1)
#ged.set_attr_graph_used('label',"")
result=HED.compare([G2,G1],None)
print(result)

bp2 = gm.BP_2(1,1,1,1)
#ged.set_attr_graph_used('label',"")
result=bp2.compare([G2,G1],None)
print(result)

greedyED =gm.GreedyEditDistance(1,1,1,1)
result=greedyED.compare([G2,G1],None)
print(result)