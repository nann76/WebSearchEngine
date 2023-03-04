import  jieba
from IdMap import IdMap
import pandas as pd
import pickle as pkl
import os
import re

dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"

url_id_map = IdMap()  # url  id map
url_linkto={}           #url的link


term_id_map=IdMap() #term  id  map

def load():

    with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
        url_id_map = pkl.load(doc)

    with open(os.path.join(dir_path, "pkl_dir/" + "url_linkto_dict.pkl"), 'rb') as doc:
        url_linkto=pkl.load(doc)


def load_content():
    '''
    num_doc=0
  #  for doc in os.listdir(dir_content_path):
    #    pass




   for doc in os.listdir(dir):
       num_doc += 1
       # 去除.txt
       pre_doc = doc.strip()[0:-4].lower()
       for term_title in pre_doc.split(' '):
           # 题目构成的词袋
           bag_words_title.append(term_title)

       # 添加doc和id的map
       doc_id = doc_id_map[doc.strip()[0:-4]]

       firstline = 1
       for line in open(dir + doc).readlines():
           if firstline == 1:
               line = line.strip()[8:].lower().split(' ')
               bag_words_author.extend(line)
               firstline = 0
           else:
               # 去除停用词
               line = line.replace(';', '')
               line = line.replace(",", '')
               line = line.replace('.', '')
               line = line.replace(':', '')
               line = line.replace('?', '')
               line = line.replace('!', '')
               line = line.replace("'s", '')
               line = line.replace("'ll", '')
               line = line.replace("'", '')
               line = line.strip().lower().split(' ')
               bag_words_content.extend(line)
'''

if  __name__ == "__main__":

    #load()
    #load_content()
    for line in open(dir_content_path+"/0.txt",'r',encoding='utf-8').readlines():
        print(line)
        str_cut=jieba.lcut_for_search(line)
        print(str_cut)





