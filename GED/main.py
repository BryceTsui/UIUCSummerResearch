import pygraphviz

from networkx.drawing import nx_agraph

import networkx as nx
dotFormat = """
digraph G{
edge [dir=forward]
node [shape=plaintext]
0 [label="0 (None)"]
0 -> 7 [label="root"]
1 [label="1 (The)"]
4 [label="4 (great Indian Circus)"]
4 -> 4 [label="compound"]
4 -> 1 [label="det"]
4 -> 4 [label="amod"]
5 [label="5 (is)"]
6 [label="6 (in)"]
7 [label="7 (Mumbai)"]
7 -> 6 [label="case"]
7 -> 5 [label="cop"]
7 -> 4 [label="nsubj"]
}
"""
import pydot
graph = pydot.graph_from_dot_file('sum3.dot')

nodes_bb = {}
graph_dot = pydot.Dot(graph_type="digraph")
graph_DD = pydot.Dot(graph_type="digraph")
graph_CD = pydot.Dot(graph_type="digraph")
graph_CFG = pydot.Dot(graph_type="digraph")

#遍历node
for cluster in graph[0].get_subgraphs():
     print(cluster.obj_dict['name'])
     if cluster.obj_dict['name'].startswith('cluster_'):
          basic_block_id = cluster.obj_dict['name'].split('_')[-1]
          print(basic_block_id)
          for node in cluster.obj_dict['nodes'].keys():
                print(cluster.obj_dict['nodes'][node][0]['attributes'])

                #nodes_bb[node] = str(basic_block_id)
                nodes_bb[node] = cluster.obj_dict['nodes'][node]
                graph_dot.add_node(cluster.get_node(node)[0])
                graph_DD.add_node(cluster.get_node(node)[0])
                graph_CD.add_node(cluster.get_node(node)[0])
                graph_CFG.add_node(cluster.get_node(node)[0])


          print("***********")

#遍历edge
# dd
# edges
# color: cyan4
# use
# edges
# color: black, dashed
# cd
# edges
# color: blue
# cfg
# edges
# color: gray
print("nodes")



for cluster in graph[0].get_subgraphs():
    print(cluster.obj_dict['name'])
    if cluster.obj_dict['name'].startswith('cluster_'):
        basic_block_id = cluster.obj_dict['name'].split('_')[-1]
        print(basic_block_id)

        for edge in cluster.get_edges():
            #print(edge.__get_attribute__('color'))
            graph_dot.add_edge(edge)
            color = edge.__get_attribute__('color')
            color = color.strip()

            print(color == '"gray"')
            print(color+" "+'gray')
            # color str contains "" in its str
            if edge.__get_attribute__('color') == '"gray"':
                print('gray')
                graph_CFG.add_edge(edge)
            if edge.__get_attribute__('color') == '"blue"':
                print('blue')
                graph_CD.add_edge(edge)
            if edge.__get_attribute__('color') == '"cyan4"':
                print('add cyan4')
                graph_DD.add_edge(edge)


        print("***********")

print(graph_dot)
print(graph_DD)

nx_g =nx.nx_pydot.from_pydot(graph_dot)
nx_CFG =nx.nx_pydot.from_pydot(graph_CFG)
nx_DD = nx.nx_pydot.from_pydot(graph_DD)
nx_CD = nx.nx_pydot.from_pydot(graph_CD)


#去除independent的node
print(nx_DD.degree())
degree = nx_DD.degree()
to_remove = [n[0] for n in degree if n[1] == 0]
print(to_remove)
nx_DD.remove_nodes_from(to_remove)
print(nx_DD.degree())


print("nx_g")
print(nx_g.nodes.get('NODE0x8767a60')['label'])

#检查是哪一个node没有label
for node in nx_g.nodes:
    print(node)
    print(nx_g.nodes.get(node));
    if not'label' in nx_g.nodes.get(node):
        nx_g.nodes.get(node)['label'] = ''
        print("relabel the attribute"+nx_g.nodes.get(node)['label'])

print('edges')
for edge in nx_g.edges:

    print(nx_g.edges.get(edge))
    print(edge)
    print(nx_g.nodes.get(edge[0]))



import matplotlib.pyplot as plt
nx.draw(nx_DD)
plt.show()
nx.drawing.nx_pydot.write_dot(nx_DD,"generate_sum3_DD.dot")
print(graph[0].get_subgraphs()[0].get_nodes())
print(graph[0].get_subgraphs())
print(graph[0].get_subgraphs()[0].obj_dict['nodes'].keys())



# graph_new = pydot.Dot(graph_type="digraph")
#
# node_a = pydot.Node("Node A", style="filled", fillcolor="red",label="123a")
# node_b = pydot.Node("Node B", style="filled", fillcolor="green",label="123b")
#
# graph_new.add_node(node_a)
# graph_new.add_node(node_b)
#
# graph_new.add_edge(pydot.Edge(node_a, node_b))
# nx_g =nx.nx_pydot.from_pydot(graph_new)
# print(nx_g.number_of_nodes())


#尝试从dot直接读，失败：
# G = nx.MultiDiGraph(nx.drawing.nx_pydot.read_dot("sum3.dot"))
# nx.drawing.nx_pydot.write_dot(G,"testsum.dot")


G1 = nx.Graph()
G1.add_node(1,label="1")
G1.add_node(2,label="2")
G1.add_node(3,label="3")
G1.add_edge(1,2)
G1.add_edge(1,3)

G2 = nx.Graph()
G2.add_node(1,label="1")
G2.add_node(3,label="3")
G2.add_node(4,label="4")
G2.add_edge(1,3)


# G2.add_node(3,label="key")
nx.drawing.nx_pydot.write_dot(G2,"generate_G2.dot")

# def compare_node(a,b):
#     return a['label']==b['label']
#
# def compare_edge(e1,e2):
#     print("edge info")
#     print(e1)
#     return False

for dis in nx.algorithms.similarity.optimize_graph_edit_distance(G1, G2, node_match=lambda a,b: a['label'] == b['label']):#params contain edge_match,but it has considered the edge but ignore the attributes in edges, in our project we can ignore the attributes in edges
    print(dis)




import gmatch4py as gm
#ged=gm.GraphEditDistance(1,1,1,1) # node del node ins edge del edge in
ged = gm.HED(1,1,1,1)
#ged.set_attr_graph_used('label',"")
result=ged.compare([G2,G1],None)
print(result)
print(ged.similarity(result))

import pydot
import pyparsing
import json


# print(G.number_of_nodes())
