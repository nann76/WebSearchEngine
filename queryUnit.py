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
# import synonyms


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


# url的id的list生成页面显示的page结构

def urlid_to_page(idlist):
    with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
        url_id_map = pkl.load(doc)

    title_df = buildIndex.read_csv(dir_path + '/' + 'title_url.csv')

    page=[]
    for id in idlist:

        page_item=[]
        page_item.append(url_id_map[id])

        index=title_df[title_df.url ==url_id_map[id]].index.tolist()[0]

        page_item.append(title_df.title.loc[index])

        for content in open(dir_content_path + '/' + str(id) + '.txt', encoding='utf-8').readlines():
            page_item.append(content[:100])

        page_item.append(id)
        page.append(page_item)

    return page



class Query:

    def __init__(self ,hobby=None):

        #content的tfidf和tfidf_vectorizer
        with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf_vectorizer.pkl'), 'rb') as doc:
            self.content_tfidf_vectorizer=pkl.load(doc)
        with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf.pkl'), 'rb') as doc:
            self.content_tfidf=pkl.load(doc)

        #url_id_map
        self.url_id_map=IdMap.IdMap()
        with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
            self.url_id_map = pkl.load(doc)

        #词袋
        with open(os.path.join(dir_path, "pkl_dir/" + 'words_bag.pkl'), 'rb') as doc:
            self.words_bag = pkl.load(doc)
        #url的pagerank
        with open(os.path.join(dir_path, "pkl_dir/" + 'pageRRank.pkl'), 'rb') as doc:
            self.pageRank = pkl.load(doc)

        self.hobby=hobby

    #个性化查询,为不同的⽤户提供不同的内容排序
    def add_personal_queries(self,qr,hobby=None,history=None,para_hobby=10,para_history=20):

        str_hobby=''
        for i in hobby:
            str_hobby+=i+' '
        str_history=''
        for i in history:
            str_history+=i+' '

        url_score_hobby=Query.common_query(self,str_hobby)
        url_score_history=Query.common_query(self,str_history)


        qr_keys=qr.keys()
        url_score_hobby_keys=url_score_hobby.keys()
        url_score_history_keys=url_score_history.keys()

        for key in url_score_hobby_keys:
            if key in qr_keys:
                qr[key]+=url_score_hobby[key]/para_hobby

        for key in url_score_history_keys:
            if key in qr_keys:
                qr[key]+=url_score_history[key]/para_history

    #个性化推荐
    # def add_personal_recommendation(self ,qr,hobby=None,history=None):
    #
    #
    #
    #     rec_hobby=[]
    #     for h in hobby:
    #         # hh=synonyms.display(h,size=3)
    #         rec_hobby.extend(synonyms.nearby(h,size=5)[0])
    #     print(rec_hobby)
    #
    #     # his=[]
    #     # for h in history:
    #     #     print(h)
    #     #     query = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), " ", h)
    #     #     query = query.lower()
    #     #     query_words = ' '.join(jieba.lcut_for_search(query))
    #     #     his.append(query_words)
    #     # print(his)
    #
    #
    #     rec_history=[]
    #     # for hh in history:
    #     #     print('hh',hh)
    #     #     h=synonyms.seg(hh)
    #     #     print(h)
    #     #     rec_history.append(synonyms.nearby(h, size=5)[0])
    #     # print(rec_history)
    #
    #
    #     st_hobby=''
    #     for temp in rec_hobby:
    #         st_hobby+=temp+' '
    #
    #     url_score=Query.common_query(self,st_hobby)
    #     after_add_personal_recommendation = dict(qr)
    #     after_add_personal_recommendation.update(url_score)
    #     print(after_add_personal_recommendation)
    #     set(after_add_personal_recommendation)
    #     return  after_add_personal_recommendation


    #pageRank的分数加权
    def add_pageRank(self,qr,para=100):
        # print(type(self.pageRank))
        # print(self.pageRank)

        for temp in qr.keys():
            # print(qr[temp],self.pageRank[temp])
            qr[temp]+=self.pageRank[temp]/para
            # print(qr[temp])

    #排序
    def query_result_sort(self,url_score):

        # 根据相关性得分排序，去除得分为0文档，其他文档按从大到小排序
        new_url_score = sorted(url_score.items(), key=lambda score: score[1], reverse=True)
        sorted_score_id = [score[0] for score in new_url_score ]
        # new_url_score = sorted(url_score.values())
        print(new_url_score)
        print(sorted_score_id)
        # return new_url_score, sorted_score_id
        return  sorted_score_id


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
        # print(query_vec)

        # vsm计算得分
        print(self.content_tfidf.shape[1])
        num_doc=self.content_tfidf.shape[0]
        score = np.zeros(num_doc)
        tf_idf=self.content_tfidf.toarray()
        # print(tf_idf)

        get_score(num_doc,score,tf_idf,query_vec)
        # print(score)

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

        return  url_score

        # # 根据相关性得分排序，去除得分为0文档，其他文档按从大到小排序
        # new_url_score = sorted(url_score.items(), key=lambda score: score[1], reverse=True)
        # sorted_score_id = [score[0] for score in new_url_score ]
        # # new_url_score = sorted(url_score.values())
        # print(new_url_score)
        # print(sorted_score_id)
        # return new_url_score,sorted_score_id


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

        return  url_score

        # print(url_score)
        # # 根据相关性得分排序，去除得分为0文档，其他文档按从大到小排序
        # new_url_score = sorted(url_score.items(), key=lambda score: score[1], reverse=True)
        # sorted_score_id = [score[0] for score in new_url_score ]
        # # new_url_score = sorted(url_score.values())
        # print(new_url_score)
        # print(sorted_score_id)
        # return new_url_score,sorted_score_id

    #短语查询
    def pharse_query(self,query,position_type):
        q_list=[]
        if position_type==0:
            q_list = buildIndex.query_Content(query)
        if position_type==1:
            q_list = buildIndex.query_Title(query)
        if position_type==2:
            q_list = buildIndex.query_Archor(query)

        query_list=[]
        for q in q_list:
            query_list.append(q['url'])

        url_list=[]
        for i in query_list:
            url_list.append(self.url_id_map[i])
        print(query_list)
        print(url_list)
        return query_list




    def query(self,input_query,query_type=0,positin_type=0,hobby=None,history=None):

        page=[[]]
        #短语查询
        if query_type==1:
            url_list=Query.pharse_query(self,query=input_query,position_type=positin_type)
            print('url_list',url_list)
            page=urlid_to_page(url_list)
            return page

        #通配查询
        if query_type==2:
            # 通配查询
            url_score=Query.wildcard_query(self,input_query)
            # 个性化查询
            Query.add_personal_queries(self,qr=url_score,hobby=hobby,history=history)
            # pageRank
            Query.add_pageRank(self,qr=url_score)
            # 得到排序后url的id的list
            sorted_score_id=Query.query_result_sort(self,url_score)
            page=urlid_to_page(sorted_score_id)
            return page



        #站内查询
        if query_type == 3:
            url_score = Query.common_query(self,input_query)

            # # 个性化推荐
            # Query.add_personal_queries(self, qr=url_score, hobby=hobby, history=history)

            # 个性化查询
            Query.add_personal_queries(self,qr=url_score,hobby=hobby,history=history)
            # pageRank
            Query.add_pageRank(self,qr=url_score)
            # 得到排序后url的id的list
            sorted_score_id=Query.query_result_sort(self,url_score)
            page=urlid_to_page(sorted_score_id)
            return page



if __name__ =="__main__":
    u=Query()


    q = "袁晓洁"
    # qr = u.common_query(q)
    qr={}
    hobby = ['本科生', '计算机科学与技术']
    history=['计算机','网络安全','南开大学关于2022年秋季学期研究生教学工作预案']
    u.add_personal_recommendation(qr,hobby=hobby,history=history)

    # q="袁晓洁"
    # # q='网络攻防与系统安全'
    # hobby=['本科生','计算机科学与技术']
    # st=''
    # for i in hobby:
    #     st+=i+' '
    # print(st)
    # qr=u.common_query(q)
    # pc=u.add_personal_recommendation(qr,st)
    # u.add_pageRank(pc)
    # u.query_result_sort(pc)



    # q2='袁*'
    # u.wildcard_query(q2)
    # q='网络攻防与系统安全'
    # u.pharse_query(q)