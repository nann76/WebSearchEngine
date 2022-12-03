import os.path
from string import punctuation
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.sorting import FieldFacet
import pickle as pkl
from IdMap import IdMap
import pandas as pd
import jieba
import re
from jieba.analyse import ChineseAnalyzer

dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"
dir_index_path="C:/Users/nan/Desktop/Web_Search_Engine/index"

#os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl')
def  read_IdMap(path):
    map=IdMap()
    with open(path, 'rb') as doc:
        map= pkl.load(doc)
    return  map

def  read_csv(path):
    doc_csv=None
    doc_csv=pd.read_csv(path,encoding="utf_8_sig")
    return  doc_csv


def build_Title_Index():

    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    title_url=read_csv(dir_path+'/'+'title_url.csv')
    title_url=title_url.values.tolist()

    schema = Schema(url=NUMERIC(stored=True), title=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_title_source')
    writer = ix.writer()

    for term in title_url:

        if term[1] != '':
           url_temp=id_map[term[2]]
           title_temp=str(term[1])
           title_temp = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", title_temp)
           title_temp = title_temp.lower()
           #words = ' '.join(jieba.lcut_for_search(title_temp))
           writer.add_document(url=url_temp, title=title_temp )
    writer.commit()

def build_Archor_Index():

    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    archor_url=read_csv(dir_path+'/'+'archor_url.csv')
    archor_url=archor_url.values.tolist()

    schema = Schema(url=NUMERIC(stored=True), archor=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_archor_source')
    writer = ix.writer()

    for term in archor_url:
            #term = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", term)
            if  term[1]!='':
                url_temp = id_map[term[2]]
                archor_temp = str(term[1])
                archor_temp = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", archor_temp)
                archor_temp = archor_temp.lower()
                #words = ' '.join(jieba.lcut_for_search(archor_temp))
                print(id_map[term[2]],term[1])
                writer.add_document(url=url_temp, archor=archor_temp )
    writer.commit()


def query_Title():
    new_list = []
    index = open_dir(dir_index_path, indexname='url_title_source')  # 读取建立好的索引

    with index.searcher() as searcher:
        parser = QueryParser("title", index.schema)
        myquery = parser.parse("南开大学")
        facet = FieldFacet("url", reverse=True)  # 按序排列搜索结果
        results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
        print(results)
        for result1 in results:
            print(dict(result1))
            new_list.append(dict(result1))
    return  new_list



if __name__ =="__main__":
    #build_Title_Index()
    #build_Archor_Index()

    print( query_Title()[0]['url'])


'''
analyser = ChineseAnalyzer()  # 导入中文分词工具
schema = Schema(phone_name=TEXT(stored=True, analyzer=analyser), price=NUMERIC(stored=True),
                phoneid=ID(stored=True))  # 创建索引结构
ix = create_in("path", schema=schema, indexname='indexname')  # path 为索引创建的地址，indexname为索引名称
writer = ix.writer()
writer.add_document(phone_name='name', price="price", phoneid="id")  # 此处为添加的内容
print("建立完成一个索引")
writer.commit()
# 以上为建立索引的过程
new_list = []
index = open_dir("indexpath", indexname='comment')  # 读取建立好的索引
with index.searcher() as searcher:
    parser = QueryParser("要搜索的项目，比如“phone_name", index.schema)
    myquery = parser.parse("搜索的关键字")
    facet = FieldFacet("price", reverse=True)  # 按序排列搜索结果
    results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
    for result1 in results:
        print(dict(result1))
        new_list.append(dict(result1))
'''