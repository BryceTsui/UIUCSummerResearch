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
  classify - the matching result of incorrect programs to correct programs'clusters
  correct - the clustering result of correct programs
  incorrect - the clustering result of incorrect programs(it is not that important, you can ignore this dir currently)
 * Work Report -My Reports about my work. You can ignore this dir. 
 * iterate -The data set used in our research. You can find checksum.c in each subdir like ```/iterate/problems/XXX/00X```
 
 
 
## Installation

To install this project, run the following commands:
```bash
git clone https://github.com/BryceTsui/UIUCSummerResearch.git
```

## Example
If you want to use the project just to calculate the graph similarity, you can just call /GED/GraphSimilarity after change the path to the data set.Note, this project only target at the data set in [iterate](https://github.com/BryceTsui/UIUCSummerResearch/tree/master/iterate). If you want to use new data set,  need to modify the program carefully. 

```bash
get_similarity('G:\\UIUC\GED\\testData\checksum1.c','G:\\UIUC\GED\\testData\checksum2.c','G:\\UIUC\DDCD\dg\\build\\tools')
```


