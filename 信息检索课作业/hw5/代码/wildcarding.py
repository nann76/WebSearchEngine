
import pickle as pkl
import os
from fnmatch import fnmatchcase as match


dir_pkl_path="C:/Users/nan/Desktop/Web_Search_Engine/data/pkl_dir"




def wildcardLookup(st, wbags):

    # see=re.compile(st)
    # matches=[string for string in wbags if re.match(see, string)]

    matches=[string for string in wbags if match( string,st)]
    # print(matches)
    return  matches



if __name__=="__main__":

    words_bag = []
    with open(os.path.join(dir_pkl_path, 'words_bag.pkl'), 'rb') as doc:
        words_bag = pkl.load(doc)

    print(words_bag)

    # w=['hello','word','aaaa','bbbbkk','0112']
    s='袁*'
    wildcardLookup(s,words_bag)