# UIUCSummerResearch
![1](https://img.shields.io/github/issues/BryceTsui/UIUCSummerResearch) ![2](https://img.shields.io/github/forks/BryceTsui/UIUCSummerResearch) ![3](https://img.shields.io/github/stars/BryceTsui/UIUCSummerResearch)

## Programs and other stuff of my summer research in UIUC

## Requirements
 * Python 3(recommend python version > 3.5)
 * ([networkx](https://github.com/networkx/networkx) (if not : `(sudo) pip(3) install networkx`)
 * ([pydot](https://github.com/pydot/pydot) (if not:`(sudo) pip(3) install pydot`)
 * ([dg](https://github.com/mchalupa/dg))
 
 ## Project
 * GED -python programs to generate the similarity of two c files(mainly depends on the GED algorithm). You'd better just call the method ```get_similarity(cfile1,cfile2,dg_tools_path)``` in GraphSimilarity.py, while other programs is just for testing. 
 (classify - the matching result of incorrect programs to correct programs'cluster
 correct - the clustering result of correct programs
 incorrect - the clustering result of incorrect programs(it is not that important, you can ignore this dir currently))
 * Work Report -My Reports about my work. You can ignore this dir. 
 * iterate -The data set used in our research. You can find checksum.c in each subdir like ```/iterate/problems/XXX/00X```
 
 
 
## Installation

To install this project, run the following commands:
```bash
git clone https://github.com/BryceTsui/UIUCSummerResearch.git
```
## Intro
### 1、compile c programs
Input: c programs
Output: dot files 
In this step, I use LLVM's tool dg to compile c programs, and then generate DD,CD,CFG graphs of these grograms. 

And your data should follow next rule:

-datasetName(could contain several problems)
--problems
---students
----all the student's submits
-----some files and one c file with the same name of problem(for example checksum.c)


### 2、generate graphs

Input: dot files
Output: Graphs(CD,DD,CFG)

In this step, you should put dot file as input and will get CD, DD,CFG graphs.

To realize this step, I use networkx, pydot in my program.

### 3、get similarity

Input: graphs
Output: similarity(0.0 - 1.0)

In this step, I use edit distance to judge the similarity between two graphs.


### run 3 steps above
I combine these three steps into one programs, so you can run them easily.
To finish these steps, you can run the main function in the GED.py file and change the parameter of 'datasetPath' to your datasetPath.

```
if __name__ == '__main__':

    datasetPath = "G:\\UIUC\IntroClass_Dot\IntroClass"

......

```

### 4、Test cases

Input: test cases
Output: Incorrect programs and correct programs

To judge weather a program is correct or incorrect, we have to use test cases to judge it. 
To help you test all programs easily and automatically, I write a program to help you do that. 

You only have to run the mian funtion in TestResult.py and change 

'names' to the names of problems(>=1)
'path' to the path of the dataset

```
if __name__ == '__main__':

    names = ['syllables']
    path = 'G:\\UIUC\IntroClass_Dot\IntroClass'
    for name in names:
        getAllResult(path, path+'\\'+name+'\\tests\whitebox\\',
                     path+'\\'+name+'\\tests\\blackbox\\',name)

```

### 5、Cluster
Input: Correct programs, Incorrect programs, Similarity Matrix
Output: All Clusters

In this step, I use AffinityPropagation Clustering Algorithm to complete this it. 

You can run main funtion in CLuster.py to finish this step.

```
if __name__ == '__main__':

    names = ['checksum']
    types = ['CFG','CD','DD']
    for name in names:
        for type in types:
                #classifyIncorrectSamples(name,type,"G:\\UIUC\IntroClass_Dot\IntroClass")
                correctClustering(name, type, "G:\\UIUC\IntroClass_Dot\IntroClass")
```



## Example
If you want to use the project just to calculate the graph similarity, you can just call /GED/GraphSimilarity after change the path to the data set.Note, this project only target at the data set in [iterate](https://github.com/BryceTsui/UIUCSummerResearch/tree/master/iterate). If you want to use new data set,  need to modify the program carefully. 

```bash
get_similarity('G:\\UIUC\GED\\testData\checksum1.c','G:\\UIUC\GED\\testData\checksum2.c','G:\\UIUC\DDCD\dg\\build\\tools')
```


