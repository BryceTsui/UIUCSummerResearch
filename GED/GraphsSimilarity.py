import os
import networkx as nx


def exe_command(work_path,command):

    """
    execute command in the terminal

    Parameters
    ----------
    work_path: str
        The path that you want to execute this command

    command: str
        The command you want to execute
    Returns
    -------
    None
    """

    #save the original dir then we can change to the original dir after executing command
    original_cwd = os.getcwd()
    print(original_cwd)
    os.chdir(work_path)
    os.system(command)

    os.chdir(original_cwd)

#like: '/home/xgy/UIUC/dg/build/tools'
def generateDotFile(cfile_path,dg_tools_path):
    """
    generate dot file from the c file

    Parameters
    ----------
    cfile_path: str
        The path of file that you want to generate dot file from.

    dg_tools_path: str
        The path of 'tools' dir of dg. You can find dg project from https://github.com/mchalupa/dg

    Returns
    -------
    array that contains path to the dot file. Default path is the same dir of the c file.
    """
    command = 'clang ' + cfile_path + ' -c -emit-llvm'  # compile file without optimizing
    # I have executed this line and generated the .bc file
    exe_command(os.path.dirname(cfile_path), command)

    # execute command looks like this: ./llvm-dg-dump  ~/UIUC/iterate-data/checksum-1.bc > ~/UIUC/iterate-data/checksum-1.dot
    command = './llvm-dg-dump ' + cfile_path.replace('.c', '.bc') + " > " + cfile_path.replace('.c', '.dot')
    exe_command(dg_tools_path,command)
    return cfile_path.replace('.c', '.dot')

def get_graphs(dotfile_path):
    """
    get four graphs from the dot file

    Parameters
    ----------
    dotfile_path: str
        The path of dot file. You need to first generate the dot file using the method generateDotFIle()

    Returns
    -------
    four graphs； the whole graph, CFG graph, DD graph and CD graph.The CFG,DD,CD graphs is a part of the whole graph
    """
    print(dotfile_path)
    print('start generate graph')
    import networkx as nx
    import pydot
    graph = pydot.graph_from_dot_file(dotfile_path)

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

    # traverse edge
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

def remove0DegreeNode(graph):

    """
    remove nodes of which degree is zero. It means these nodes have no edge.

    Parameters
    ----------
    graph: a networkx.Graph, networkx.DiGraph or networkx.MultiDiGraph
        You can generate these graph by calling the get graphs method

    Returns
    -------
    graph removing the 0 degree nodes
    """

    print('start remove 0 degree nodes')
    degree = graph.degree()
    to_remove = [n[0] for n in degree if n[1] == 0]
    graph.remove_nodes_from(to_remove)
    print('end remove 0 degree nodes')
    return graph

def getEditDistanceWithoutLabel(graph1,graph2):
    """
    get edit distance without consideration of label. It means this method does not consider the label of each node and only
    calculate the edit distance to transfer graph1 to graph2 with the same structure but permise all nodes have the corresponding
    labels.

    Example:

    node1 : key:1 label:'add', node2: key:2, label'add'. This method with treat these two nodes as two different nodes,regradless
    of they have the same label. If you want method considering these two nodes as the same, you need to use the getEditDistanceWithLabel

    Parameters
    ----------
    graph1,graph2: networkx.Graph, networkx.DiGraph or networkx.MultiDiGraph
        Two graphs you want to get the edit distance between them.

    Returns
    -------
    float representing the edit distance of this two graphs
    """
    all = 0;
    n = 0;
    for dis in nx.algorithms.similarity.optimize_graph_edit_distance(graph1,graph2,node_match=lambda a,b:True):  # params contain edge_match,but it has considered the edge but ignore the attributes in edges, in our project we can ignore the attributes in edges
        all = all +dis
        n = n+1

    return all/n

def checkNullLabel(graph):
    """
    give value to the nodes which have no attribute 'label'

    Parameters
    ----------
    graph: networkx.Graph, networkx.DiGraph or networkx.MultiDiGraph

    Returns
    -------
    graph after transferring
    """
    for node in graph.nodes:
        if not 'label' in graph.nodes.get(node):
            graph.nodes.get(node)['label'] = ''
    return graph


def getOpCode(label):
    """
    get Operator code from the label str. This method is used to get the main Opcode from the label of nodes. You can modify
    this method to suit your project.

    Example:

        label="main::
        %3 = alloca i32, align 4"

        This method will return alloca.

        label="main::
        store i32 0, i32* %1, align 4"

        This method will return store.

        Because I cannot know the exact grammar rule of the label, so I just extract opcode following such rules:

            "XXX
                XXX = Opcode ...."
                or
            "XXX
                Opcode = ..... "
                or
            ""
        Note that if the label does not follow such rules, this method will return "*" to represent unknown Opcode

    Parameters
    ----------
    label: str
        the Label of node

    Returns
    -------
    str. the Opcode of this label
    """
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
    return getOpCode(a['label'])== getOpCode(b['label'])

def getEditDistanceWithLabel(graph1,graph2):
    """
    get edit distance with consideration of label. It means this method considers the label of each node and
    calculate the edit distance to transfer graph1 to graph2 with the same corresponding label.

    Example:

    node1 : key:1 label:'add', node2: key:2, label'add'. This method with treat these two nodes as the same.
     If you want method considering these two nodes as different nodes, you need to use the getEditDistanceWithoutLabel

    Parameters
    ----------
    graph1,graph2: networkx.Graph, networkx.DiGraph or networkx.MultiDiGraph
        Two graphs you want to get the edit distance between them.

    Returns
    -------
    float. representing the edit distance of this two graphs
    """
    graph1 = checkNullLabel(graph1)
    graph2= checkNullLabel(graph2)
    all = 0;
    n = 0;
    for dis in nx.algorithms.similarity.optimize_graph_edit_distance(graph1,graph2,node_match=__node_match__):  # params contain edge_match,but it has considered the edge but ignore the attributes in edges, in our project we can ignore the attributes in edges
        all = all + dis
        n = n + 1

    return all / n

def getMaxLen(graph1,graph2):
    return max((len(graph1.nodes)+len(graph1.edges)),(len(graph2.nodes)+len(graph2.edges)))

#cfile_path1 is the path of the first c file
#cfile_path2 is the path of the second c file
def get_similarity(cfile_path1, cfile_path2,dg_tools_path,label=False):
    """
    The main method of this file. If you just want to get the similarity of two graphs, you can just call this method.

    Parameters
    ----------
    cfile_path1,cfile_path2: str
        The path of two c file.

    dg_tools_path: str
        The path of 'tools' dir of dg. You can find dg project from https://github.com/mchalupa/dg

    label: bool
        Whether you want to take label into consideration? Default value is False.

        If the label is False: Node1{key:1,label:'add'} and Node2{key:2,label:'add} will be treated as different nodes.
            and  Node1{key:1,label:'add'} and Node{key:1,label:'mul} will be treated as the same.

        If the label is True. The judgement above will be reversed.

    Returns
    -------
    float. The similarity of two graphs
    """
    # generate dot file from the paths
    dotfile_path1 = generateDotFile(cfile_path1,dg_tools_path)
    dotfile_path2 = generateDotFile(cfile_path2,dg_tools_path)

    # extract graphs from the dot files
    whole_graph1,CFG1,DD1,CD1 = get_graphs(dotfile_path1)
    whole_graph2,CFG2,DD2,CD2 = get_graphs(dotfile_path2)

    # remove useless nodes from the graphs
    whole_graph1, CFG1, DD1, CD1 = remove0DegreeNode(whole_graph1),remove0DegreeNode(CFG1),remove0DegreeNode(DD1),remove0DegreeNode(CD1)
    whole_graph2, CFG2, DD2, CD2 = remove0DegreeNode(whole_graph2), remove0DegreeNode(CFG2), remove0DegreeNode(DD2), remove0DegreeNode(CD2)

    # if not considering the label
    if not label:
        return getEditDistanceWithoutLabel(whole_graph1,whole_graph2)/getMaxLen(whole_graph1,whole_graph2),getEditDistanceWithoutLabel(CFG1,CFG2)/getMaxLen(CFG1,CFG2),getEditDistanceWithoutLabel(DD1,DD2)/getMaxLen(DD1,DD2),getEditDistanceWithoutLabel(CD1,CD2)/getMaxLen(CD1,CD2)

    # if considering the label
    else:
        return getEditDistanceWithLabel(whole_graph1, whole_graph2)/getMaxLen(whole_graph1,whole_graph2), getEditDistanceWithLabel(CFG1,CFG2)/getMaxLen(CFG1,CFG2), getEditDistanceWithLabel(DD1, DD2)/getMaxLen(DD1,DD2), getEditDistanceWithLabel(CD1, CD2)/getMaxLen(CD1,CD2)



#test the method get_similarity()
if __name__ == '__main__':
    print(get_similarity('G:\\UIUC\GED\\testData\checksum1.c','G:\\UIUC\GED\\testData\checksum2.c','G:\\UIUC\DDCD\dg\\build\\tools'))

