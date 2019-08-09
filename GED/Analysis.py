
if __name__ == '__main__':

    # import methods from the GED.py
    from GED import get_graphs,remove0DegreeNode,extractDotFile

    #the path to the 'problems' dir
    dot_files = extractDotFile("G:\\UIUC\data\iterate\problems")
    print(dot_files)

    #store all graphs including CFG,DD，CD and their dot file path
    graphs_list=[]

    #all g graphs
    g_list = []
    for dot_file in dot_files:

        g,CFG,DD,CD = get_graphs(dot_file)
        g,CFG,DD,CD = remove0DegreeNode(g),remove0DegreeNode(CFG),remove0DegreeNode(DD),remove0DegreeNode(CD)

        graphs_list.append([dot_file,g,CFG,DD,CD])
        g_list.append(g)




    n = 4 # 1=g ,2 = CFG 3= DD, 4 = CD
    file = open('data-CD-withLabel.txt', 'r')
    data = file.read()
    file.close()

    data = data.replace(" ","")
    data= data[1:len(data)-1]

    import re
    data_array = re.split('\]|\[',data)
    print(data_array)

    matrix = []

    i  =0

    for line in data_array:
        if(len(line) >=2):
            values_arr = line.split(',')
            print(len(values_arr))
            matrix.append([float(values_arr[j])/max((len(graphs_list[i][n].nodes)+len(graphs_list[i][n].edges)),(len(graphs_list[j][n].nodes)+len(graphs_list[j][n].edges))) for j in range(0,len(values_arr))])

            i = i+1


    print(len(matrix))
    print(len(matrix[0]))

    max_i =0
    max_j = 0
    max = 0.0
    f = open('csv-CD-withLabel.csv','w')

    f.write('file1/file2,')
    for file_name in dot_files:
        f.write(file_name)
        f.write(',')
    f.write('\n')
    for i in range(0,69):
        f.write(dot_files[i])
        f.write(',')
        for j in range(0,69):
            f.write(str(matrix[i][j]))
            if j != 68:
                f.write(',')
        f.write('\n')
    f.close()



    print(max)
    print(dot_files[max_i])
    print(dot_files[max_j])








