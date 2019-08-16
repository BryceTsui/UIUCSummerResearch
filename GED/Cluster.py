
from sklearn.cluster import SpectralClustering,AffinityPropagation
import numpy as np
import json
import os
def getAllSubmits(root):


    submit_path = [];
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
                                if not content.startswith('.') and content.endswith('.c'):
                                    #print(content)
                                    submit_path.append(submit_dir_path)

    return submit_path

def readLabelsResult(isWhiteBox = True):

    if isWhiteBox:
        path = 'labels_whitebox.json'
    else:
        path = 'labels_blackbox.json'

    with open(path,'r') as f:
        result = json.load(f)

    return result


def getSubMatrix(matrix,indexs):
    subMatrix = []
    for i in indexs:
        line_i = []
        for j in indexs:
            line_i.append(matrix[i][j])
        subMatrix.append(line_i)
    return np.array(subMatrix)

def cluster(names,simi_matrix,threshold):
    cluster_result = [];


if __name__ == '__main__':

    with open('data-simi-DD-withoutLabel.json','r') as f:
        data = json.load(f)
    X = np.array(data)
    print(X)

    submit_files = getAllSubmits('G:\\UIUC\data\iterate\problems')
    print(submit_files)

    white_box_result = readLabelsResult();
    print(white_box_result)
    black_box_result = readLabelsResult(isWhiteBox=False)
    print(black_box_result)

    all_pass_submits = []
    index = 0
    for submit in submit_files:
        r1 =  black_box_result[submit]
        r2 = white_box_result[submit]

        isAllPass = True;
        for i in r1:
            if r1[i]!= 1:
                isAllPass=False
        for i in r2:
            if r2[i]!=1:
                isAllPass=False

        if isAllPass:
            all_pass_submits.append(index)

        index = index+1



    all_pass_matrxi = getSubMatrix(X,all_pass_submits)
    all_pass_matrxi = all_pass_matrxi


    for i in range(0,len(all_pass_submits)):
        print(str(i)+" "+str(submit_files[all_pass_submits[i]]))


    sc = SpectralClustering(3, affinity='precomputed', n_init=69)
    sc.fit(all_pass_matrxi)

    ap = AffinityPropagation().fit(all_pass_matrxi)



    print(sc.labels_)
    print(ap.labels_)

    i= 0
    clustering_result = {}
    for label in ap.labels_:
        if not label in clustering_result:
            clustering_result[label] = [submit_files[all_pass_submits[i]]]
        else:
            clustering_result[label].append(submit_files[all_pass_submits[i]])
        i= i+1

    for key in clustering_result:
        code_detail = ''
        for file in clustering_result[key]:
            code_detail = code_detail+ file+ ':\r\n'
            with open(file+"\\"+'checksum.c','r')as f:
                code_detail = code_detail+f.read()
                f.close()

        with open('cluster_result/label_'+str(key)+'DD.txt','w') as f:
            f.write(code_detail)
            f.close()

