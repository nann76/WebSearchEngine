import os
import pickle as pkl
from IdMap import IdMap
import networkx as nx
import matplotlib.pyplot as plt


dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"
dir_index_path="C:/Users/nan/Desktop/Web_Search_Engine/index"

def read_url_linkto():
    temp={}
    with open(os.path.join(dir_pkl_path,'url_linkto_dict.pkl'),'rb') as doc:
        temp=pkl.load(doc)

    return  temp

def pageRank():
    url_linkto=read_url_linkto()
    G=nx.DiGraph()
    #加边
    for i in url_linkto:
            for j in url_linkto[i]:
                G.add_edge(i,j)
    #计算，阻尼因子 0.85
    pr = nx.pagerank(G, alpha=0.85)
    print(pr)
    prdic = {}
    for node, pageRankValue in pr.items():
            prdic[node] = pageRankValue * 1e4
    print(prdic)

    #序列化

    with open(os.path.join(dir_pkl_path , 'pageRRank.pkl'), 'wb') as doc:
        pkl.dump(prdic, doc)



if __name__=="__main__":

    pageRank()
