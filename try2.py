from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import re
import pickle as pkl
from string import punctuation
import os
import  numpy as np
import  IdMap
import array
import wildcarding
import buildIndex
import pandas as pd
dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"

def  read_csv(path):
    doc_csv=None
    doc_csv=pd.read_csv(path,encoding="utf_8_sig")
    return  doc_csv

with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
    url_id_map = pkl.load(doc)
    list=[]
for i in range(100):
    list.append(url_id_map[i])

d=read_csv(dir_path+'/'+'title_url.csv')
qq=d[d.url == 'http://cc.nankai.edu.cn/13274/list.htm'].index.tolist()[0]
print(qq)
print(d.title.loc[qq])


for content in open(dir_content_path + '/' + str(2)+'.txt', encoding='utf-8').readlines():
    print(content)


