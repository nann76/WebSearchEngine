from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import re
import pickle as pkl
from string import punctuation
import os
import  numpy as np
dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
dir_content_path="C:/Users/nan/Desktop/Web_Search_Engine/data/content"
dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"

with open(os.path.join(dir_path, "pkl_dir/" + 'tfidf_vectorizer.pkl'), 'rb') as doc:
    tfidf_vectorizer=pkl.load(doc)


# query=['南开大学','0061','龚克','0061']
query='南开大学'
query = re.sub(r"[{}、，。！？·【】）》；;《“”（-]+".format(punctuation), " ", query)
query = query.lower()
query_words = ' '.join(jieba.lcut_for_search(query))
query = []
query.append(query_words)
print(query)
new_term_freq_matrix = tfidf_vectorizer.transform(query)
print(new_term_freq_matrix)
query_vec = np.array((new_term_freq_matrix.todense().tolist())[0])
print(query_vec)
