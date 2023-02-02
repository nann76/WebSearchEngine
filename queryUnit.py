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

dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"

# with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf_vectorizer.pkl'), 'rb') as doc:
#     tfidf_vectorizer=pkl.load(doc)
#
#
# # query=['南开大学','0061','龚克','0061']
# query='南开大学'
# query = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), " ", query)
# query = query.lower()
# query_words = ' '.join(jieba.lcut_for_search(query))
# query = []
# query.append(query_words)
# print(query)
# new_term_freq_matrix = tfidf_vectorizer.transform(query)
# print(new_term_freq_matrix)
# query_vec = np.array((new_term_freq_matrix.todense().tolist())[0])
# print(query_vec)

# cos
def cosine_similarity(x, y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom


# 分数计算
def get_score(len, score, tf_idf_x, query):
    for i in range(len):
        # doc_vec = np.array(tf_idf_x[i])
        # print(doc_vec)
        score[i] = cosine_similarity(tf_idf_x[i], query)


class Query:

    def __init__(self):
        with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf_vectorizer.pkl'), 'rb') as doc:
            self.content_tfidf_vectorizer=pkl.load(doc)

        with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf.pkl'), 'rb') as doc:
            self.content_tfidf=pkl.load(doc)

        self.url_id_map=IdMap.IdMap()

        with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
            self.url_id_map = pkl.load(doc)

        with open(os.path.join(dir_path, "pkl_dir/" + 'words_bag.pkl'), 'rb') as doc:
            self.words_bag = pkl.load(doc)


    #常规站内查找
    def common_query(self,query):
        # 输入文本处理
        query = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), " ", query)
        query = query.lower()
        query_words = ' '.join(jieba.lcut_for_search(query))
        query = []
        query.append(query_words)
        print(query)

        # 得到输入向量
        new_term_freq_matrix = self.content_tfidf_vectorizer.transform(query)
        print(new_term_freq_matrix)
        query_vec = np.array((new_term_freq_matrix.todense().tolist())[0])
        print(query_vec)

        # vsm计算得分
        print(self.content_tfidf.shape[1])
        num_doc=self.content_tfidf.shape[0]
        score = np.zeros(num_doc)
        tf_idf=self.content_tfidf.toarray()
        print(tf_idf)

        get_score(num_doc,score,tf_idf,query_vec)
        print(score)

        list_url_id = []
        list_url=[]
        url_score={}

        #得到得分大于零的url
        for i in range(num_doc):
            if   score[i]>0:
                url_score[i]=score[i]
                list_url_id.append(i)
                list_url.append(self.url_id_map[i])

        set(list_url)
        set(list_url_id)
        set(url_score)

        print(url_score)
        # 根据相关性得分排序，去除得分为0文档，其他文档按从大到小排序
        new_url_score = sorted(url_score.items(), key=lambda score: score[1], reverse=True)
        sorted_score_id = [score[0] for score in new_url_score ]
        # new_url_score = sorted(url_score.values())
        print(new_url_score)
        print(sorted_score_id)
        return new_url_score,sorted_score_id


    #通配查找
    def wildcard_query(self,query):

        #通配根据输入在词袋中查找匹配的term
        query=wildcarding.wildcardLookup(query,self.words_bag)
        print(query)

        # 得到输入向量
        new_term_freq_matrix = self.content_tfidf_vectorizer.transform(query)
        print(new_term_freq_matrix)
        query_vec = np.array((new_term_freq_matrix.todense().tolist())[0])
        print(query_vec)

        # vsm计算得分
        print(self.content_tfidf.shape[1])
        num_doc=self.content_tfidf.shape[0]
        score = np.zeros(num_doc)
        tf_idf=self.content_tfidf.toarray()
        print(tf_idf)

        get_score(num_doc,score,tf_idf,query_vec)
        print(score)

        list_url_id = []
        list_url=[]
        url_score={}

        #得到得分大于零的url
        for i in range(num_doc):
            if   score[i]>0:
                url_score[i]=score[i]
                list_url_id.append(i)
                list_url.append(self.url_id_map[i])

        set(list_url)
        set(list_url_id)
        set(url_score)

        print(url_score)
        # 根据相关性得分排序，去除得分为0文档，其他文档按从大到小排序
        new_url_score = sorted(url_score.items(), key=lambda score: score[1], reverse=True)
        sorted_score_id = [score[0] for score in new_url_score ]
        # new_url_score = sorted(url_score.values())
        print(new_url_score)
        print(sorted_score_id)
        return new_url_score,sorted_score_id

    #短语查询
    def pharse_query(self,query):
        q_list=buildIndex.query_Content(query)

        query_list=[]
        for q in q_list:
            query_list.append(q['url'])

        url_list=[]
        for i in query_list:
            url_list.append(self.url_id_map[i])
        print(query_list)
        print(url_list)





if __name__ =="__main__":
    u=Query()

    q="袁晓洁"
    q='网络攻防与系统安全'
    u.common_query(q)
    # q2='袁*'
    # u.wildcard_query(q2)
    q='网络攻防与系统安全'
    u.pharse_query(q)