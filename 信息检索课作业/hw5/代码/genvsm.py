from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import re
import pickle as pkl
from string import punctuation
import os
from jieba.analyse import ChineseAnalyzer
dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"
import buildIndex


max_doc=108

def csv_process():

    with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
        url_id_map = pkl.load(doc)
    title_df = buildIndex.read_csv(dir_path + '/' + 'title_url.csv')
    archor_df= buildIndex.read_csv(dir_path + '/' + 'archor_url.csv')
    title_df = title_df.values.tolist()
    archor_df = archor_df.values.tolist()

    title_dict={}
    for term in title_df:
        title_dict[url_id_map[term[2]]]=term[1]
    print(title_dict)
    sorted(title_dict)
    print(title_dict)

    archor_dict={}
    for term in archor_df:
        archor_dict[url_id_map[term[2]]]=term[1]
    print(archor_dict)
    sorted(archor_dict)
    print(archor_dict)
    return title_dict,archor_dict


def genContentVSM():
    doc_list = []
    url_list = []
    temp_doc=0

    #for doc in os.listdir(dir_content_path):
    while temp_doc<max_doc:
        doc=str(temp_doc)+'.txt'
        print(dir_content_path + '/'+doc)

        try:
            for content in open(dir_content_path + '/' + doc, encoding='utf-8').readlines():
                # print(content)
                content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", content)
                content = content.lower()
                # words=jieba.lcut_for_search(content)
                words = ' '.join(jieba.lcut_for_search(content))
                # print(len(words))
                doc_list.append(words)
                # print(words)
        except:
            content = ' '
            words = ' '.join(jieba.lcut_for_search(content))
            doc_list.append(words)
            temp_doc += 1
            url_list.append(doc[0:-4])
            continue

        # for content in open(dir_content_path + '/'+doc,encoding='utf-8').readlines():
        #     #print(content)
        #     content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", content)
        #     content = content.lower()
        #     #words=jieba.lcut_for_search(content)
        #     words = ' '.join(jieba.lcut_for_search(content))
        #     #print(len(words))
        #     doc_list.append(words)
        #     #print(words)
        #url_list.append(doc[0:-4])
        temp_doc+=1

    #print(doc_list)
    '''
    # step 1
    vectoerizer = CountVectorizer(min_df=1, max_df=1.0, token_pattern='\\b\\w+\\b')
    # step 2
    vectoerizer.fit(doc_list)
    # step 3
    bag_of_words = vectoerizer.get_feature_names()
    print(bag_of_words)
    '''
    tfidf_vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc_list)
    print(tfidf_matrix)
    print(tfidf_vectorizer.get_feature_names_out())

    # print(tfidf_vectorizer.get_feature_names_out().shape)

    with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf_vectorizer.pkl'), 'wb') as doc:
         pkl.dump(tfidf_vectorizer, doc)

    with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf.pkl'), 'wb') as doc:
         pkl.dump(tfidf_matrix, doc)

    with open(os.path.join(dir_path, "pkl_dir/" + 'words_bag.pkl'), 'wb') as doc:
        pkl.dump(tfidf_vectorizer.get_feature_names_out(), doc)


def gen_Title_Archor_VSM():


    title_dict,archor_dict=csv_process()

    title_list=[]
    for term in title_dict.keys():
        content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", title_dict[term])
        content = content.lower()
        words = ' '.join(jieba.lcut_for_search(content))

        title_list.append(words)
    print(title_list)

    archor_list = []
    w = ' '.join(jieba.lcut_for_search(' '))
    archor_list.append(w)
    for term in archor_dict.keys():
        # if term>250:
        #     break
        content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", archor_dict[term])
        content = content.lower()
        words = ' '.join(jieba.lcut_for_search(content))

        archor_list.append(words)
    print(archor_list)


    t_tfidf_vectorizer = TfidfVectorizer(min_df=1)
    t_tfidf_matrix = t_tfidf_vectorizer.fit_transform(title_list)
    print(t_tfidf_matrix)
    print(t_tfidf_vectorizer.get_feature_names_out())


    a_tfidf_vectorizer = TfidfVectorizer(min_df=1)
    a_tfidf_matrix = a_tfidf_vectorizer.fit_transform(archor_list)
    print(a_tfidf_matrix)
    print(a_tfidf_vectorizer.get_feature_names_out())



    with open(os.path.join(dir_path, "pkl_dir/" + 'title_tfidf_vectorizer_matrix.pkl'), 'wb') as doc:
         pkl.dump((t_tfidf_vectorizer,t_tfidf_matrix), doc)

    with open(os.path.join(dir_path, "pkl_dir/" + 'archor_tfidf_vectorizer_matrix.pkl'), 'wb') as doc:
         pkl.dump((a_tfidf_vectorizer,a_tfidf_matrix), doc)





if __name__=="__main__":
    genContentVSM()
    # gen_Title_Archor_VSM()