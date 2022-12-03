import os.path
from string import punctuation
from whoosh.qparser import QueryParser
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer
from whoosh.sorting import FieldFacet
import pickle as pkl
from IdMap import IdMap
import pandas as pd
import jieba
import re
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
    '''
    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    title_url=read_csv(dir_path+'/'+'title_url.csv')
    title_url=title_url.values.tolist()
    '''

    schema = Schema(url=NUMERIC(stored=True), title=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='try')
    writer = ix.writer()

    writer.add_document(url=0, title="我是爱南开的" )
    #writer.add_document(url=0, title="2 bb words")
    writer.commit()

def query_Title():
    new_list = []
    index = open_dir(dir_index_path, indexname='try')  # 读取建立好的索引

    with index.searcher() as searcher:
        parser = QueryParser("title", index.schema)
        myquery = parser.parse("南开")
        #facet = FieldFacet("url", reverse=True)  # 按序排列搜索结果
        #results = searcher.search(myquery, limit=None, sortedby=facet)  # limit为搜索结果的限制，默认为10，详见博客开头的官方文档
        results=searcher.search(myquery)
        print(results)
        for result1 in results:
            print(dict(result1))
            new_list.append(dict(result1))
    return  new_list



if __name__ =="__main__":
    build_Title_Index()


    print( query_Title())