import pandas as pd
import pickle as pkl
import  os

users_dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/users"
class UserUnit:


    def __init__(self):
        self.username=[]
        self.password=[]
        self.histort_of_search=[[]]
        self.usr_pd = {}
        self.usr_hs = {}
    def load(self):

        with open(os.path.join(users_dir_path,  'usr_pd.pkl'), 'rb') as doc:
            self.usr_pd =pkl.load( doc)
        with open(os.path.join(users_dir_path,  'usr_hs.pkl'), 'rb') as doc:
            self.usr_hs=pkl.load( doc)


    def save(self,pd,hs):
        # df1 = pd.DataFrame(data=url_archor_list, columns=["username", "password","histort_of_search"])
        # df1.to_csv(os.path.join(dir_path, 'archor_url.csv'), encoding='utf_8_sig')
        self.usr_pd=pd
        self.usr_hs=hs
        with open(os.path.join(users_dir_path,  'usr_pd.pkl'), 'wb') as doc:
            pkl.dump(self.usr_pd, doc)
        with open(os.path.join(users_dir_path,  'usr_hs.pkl'), 'wb') as doc:
            pkl.dump(self.usr_hs, doc)

