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

def genContentVSM():
    doc_list = []
    url_list = []
    for doc in os.listdir(dir_content_path):
        print(dir_content_path + '/'+doc)
        for content in open(dir_content_path + '/'+doc,encoding='utf-8').readlines():
            #print(content)
            content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", content)
            content = content.lower()
            #words=jieba.lcut_for_search(content)
            words = ' '.join(jieba.lcut_for_search(content))
            #print(len(words))
            doc_list.append(words)
            #print(words)
        url_list.append(doc[0:-4])

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
    print(tfidf_vectorizer.get_feature_names_out().shape)

if __name__=="__main__":
    genContentVSM()