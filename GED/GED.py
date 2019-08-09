import os



def checkNullLabel(graph):
    for node in graph.nodes:
        if not 'label' in graph.nodes.get(node):
            graph.nodes.get(node)['label'] = ''
    return graph


def getOpCode(label):

    if label == '':
        return ''
    #! if the label looks like 'main::\n  xxxxxxxx"'
    if('\n' in label):
        #print(label)
        part2  = label.split('\n')[1]
        part2 = part2.strip()
        if(part2.startswith('%')):
            #print(part2)
            part2 = part2.split("=")[1]
            part2 = part2.strip()
            return_value = part2.split(' ')[0]

            return return_value
        else:
            part2 = part2.strip()
            return part2.split(" ")[0]

    else:
        print("cannot figure out:"+label)
        return '*'


def __node_match__(a, b):
    return getOpCode(a['label'])==getOpCode(b['label'])


def get_graphs(dotfile):

    print(dotfile)
    print('start generate graph')
    import networkx as nx
    import pydot
    graph = pydot.graph_from_dot_file(dotfile)

    nodes_bb = {}
    graph_dot = pydot.Dot(graph_type="digraph")
    graph_DD = pydot.Dot(graph_type="digraph")
    graph_CD = pydot.Dot(graph_type="digraph")
    graph_CFG = pydot.Dot(graph_type="digraph")

    # traverse node
    for cluster in graph[0].get_subgraphs():
        #print(cluster.obj_dict['name'])
        if cluster.obj_dict['name'].startswith('cluster_'):
            basic_block_id = cluster.obj_dict['name'].split('_')[-1]
            #print(basic_block_id)
            for node in cluster.obj_dict['nodes'].keys():
                #print(cluster.obj_dict['nodes'][node][0]['attributes'])

                # nodes_bb[node] = str(basic_block_id)
                nodes_bb[node] = cluster.obj_dict['nodes'][node]
                graph_dot.add_node(cluster.get_node(node)[0])
                graph_DD.add_node(cluster.get_node(node)[0])
                graph_CD.add_node(cluster.get_node(node)[0])
                graph_CFG.add_node(cluster.get_node(node)[0])

            print("***********")

    # 遍历edge
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


    for cluster in graph[0].get_subgraphs():
        #print(cluster.obj_dict['name'])
        if cluster.obj_dict['name'].startswith('cluster_'):
            basic_block_id = cluster.obj_dict['name'].split('_')[-1]
            #print(basic_block_id)

            for edge in cluster.get_edges():
                # print(edge.__get_attribute__('color'))
                graph_dot.add_edge(edge)
                color = edge.__get_attribute__('color')
                color = color.strip()

                #print(color == '"gray"')
                #print(color + " " + 'gray')
                # color str contains "" in its str
                if edge.__get_attribute__('color') == '"gray"':
                    #print('gray')
                    graph_CFG.add_edge(edge)
                if edge.__get_attribute__('color') == '"blue"':
                    #print('blue')
                    graph_CD.add_edge(edge)
                if edge.__get_attribute__('color') == '"cyan4"':
                    #print('add cyan4')
                    graph_DD.add_edge(edge)

            print("***********")

    #print(graph_dot)
    #print(graph_DD)

    nx_g = nx.nx_pydot.from_pydot(graph_dot)
    nx_CFG = nx.nx_pydot.from_pydot(graph_CFG)
    nx_DD = nx.nx_pydot.from_pydot(graph_DD)
    nx_CD = nx.nx_pydot.from_pydot(graph_CD)

    print('end generate graph')
    return nx_g,nx_CFG,nx_DD,nx_CD

def extractDotFile(root):


    dot_files = [];
    for problem in os.listdir(root):

        problem_path = os.path.join(root, problem)

        if os.path.isdir(problem_path):
            #print("problem"+problem)
            for student_dir in os.listdir(problem_path):
                #print(student_dir)

                student_dir_path = os.path.join(problem_path,student_dir)
                if os.path.isdir(student_dir_path):
                    #print("student:"+student_dir)

                    for submit_dir in os.listdir(student_dir_path):

                        submit_dir_path = os.path.join(student_dir_path,submit_dir)
                        #print(submit_dir_path)
                        if os.path.isdir(submit_dir_path):
                            #print("submit time:"+submit_dir)

                            for content in os.listdir(submit_dir_path):
                                if not content.startswith('.') and content.endswith('.dot'):
                                    #print(content)
                                    content_path = os.path.join(submit_dir_path,content)
                                    dot_files.append(content_path)

    return dot_files

def remove0DegreeNode(graph):
    print('start remove 0 degree nodes')
    degree = graph.degree()
    to_remove = [n[0] for n in degree if n[1] == 0]
    graph.remove_nodes_from(to_remove)
    print('end remove 0 degree nodes')
    return graph
if __name__ == '__main__':
    import networkx as nx
    g1,CFG1,DD1,CD1 = get_graphs('iterate-data/checksum-1.dot')

    g2,CFG2,DD2,CD2 = get_graphs('iterate-data/checksum-2.dot')
    g1, CFG1, DD1, CD1 = remove0DegreeNode(g1),remove0DegreeNode(CFG1),remove0DegreeNode(DD1),remove0DegreeNode(CD1)
    g2, CFG2, DD2, CD2 = remove0DegreeNode(g2), remove0DegreeNode(CFG2), remove0DegreeNode(DD2), remove0DegreeNode(CD2)
    print(str(len(g1.nodes)) + " " + str(len(CFG1.nodes)) + " " + str(len(DD1.nodes)) + " " + str(len(CD1.nodes)))
    print(str(len(g2.nodes)) + " " + str(len(CFG2.nodes)) + " " + str(len(DD2.nodes)) + " " + str(len(CD2.nodes)))
    for dis in nx.algorithms.similarity.optimize_graph_edit_distance(CFG1, CFG2):  # params contain edge_match,but it has considered the edge but ignore the attributes in edges, in our project we can ignore the attributes in edges
        print(dis)

    dot_files = extractDotFile("G:\\UIUC\data\iterate\problems")


    graphs_list=[]

    g_list = []




    for dot_file in dot_files:

        #get graphs from dot file
        g,CFG,DD,CD = get_graphs(dot_file)
        g,CFG,DD,CD = remove0DegreeNode(g),remove0DegreeNode(CFG),remove0DegreeNode(DD),remove0DegreeNode(CD)
        g,CFG,DD,CD = checkNullLabel(g),checkNullLabel(CFG),checkNullLabel(DD),checkNullLabel(CD)
        graphs_list.append([dot_file,g,CFG,DD,CD])
        g_list.append(g)


    print(graphs_list)


    import time

    start = time.clock()

    distances = []

    i=0
    j=0

    opCodesSet = set()
    for g in graphs_list:
        for node in g[1].nodes:
            opCodesSet.add(getOpCode(g[1].nodes.get(node)['label']))

    print(opCodesSet)


    for graphs1 in graphs_list:
        j=0
        raw = [];
        for graphs2 in graphs_list:
            if graphs1 != graphs2:#except the equal graph

                # print(len(graphs1[4].nodes))
                # print(len(graphs2[4].nodes))
                # print(len(graphs1[4].edges))
                # print(len(graphs2[4].edges))
                minv = 0;
                for dis in nx.algorithms.similarity.optimize_graph_edit_distance(graphs1[3], graphs2[3],node_match=__node_match__):
                    print("#",end="")
                    minv = dis
                print()
                raw.append(minv)
            else:
                raw.append(0.0)
            j = j + 1

        distances.append(raw)
        i = i + 1


    print(distances)
    # import gmatch4py as gm
    # import json
    # bp2 = gm.BP_2(1, 1, 1, 1)
    # # ged.set_attr_graph_used('label',"")
    # result = []#bp2.compare(g_list, None)
    # print(result)

    # file = open('data1.txt', 'w')
    # file.write(json.dumps(result));
    # file.close()

    print("time cost:")
    print(time.clock()-start)

    # import json
    # file = open('data-CD-withLabel.txt', 'w')
    # file.write(json.dumps(distances));
    # file.close()






