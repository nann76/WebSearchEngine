import pandas as pd
import pickle as pkl
import  os

users_dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/users"
class UserUnit:


    def __init__(self):
        # self.username=[]
        # self.password=[]
        # self.histort_of_search=[[]]
        self.user='root'
        self.usr_pd = {}
        self.usr_hobby={}
        self.usr_hs = {}
    def load(self):

        with open(os.path.join(users_dir_path,  'usr_pd.pkl'), 'rb') as doc:
            self.usr_pd =pkl.load( doc)
        with open(os.path.join(users_dir_path,  'usr_hs.pkl'), 'rb') as doc:
            self.usr_hs=pkl.load( doc)
        with open(os.path.join(users_dir_path,  'usr_hobby.pkl'), 'rb') as doc:
            self.usr_hobby=pkl.load( doc)

    def save(self):
        # df1 = pd.DataFrame(data=url_archor_list, columns=["username", "password","histort_of_search"])
        # df1.to_csv(os.path.join(dir_path, 'archor_url.csv'), encoding='utf_8_sig')
        # self.usr_pd=pd
        # self.usr_hs=hs
        # self.usr_hobby=hobby
        with open(os.path.join(users_dir_path,  'usr_pd.pkl'), 'wb') as doc:
            pkl.dump(self.usr_pd, doc)
        with open(os.path.join(users_dir_path,  'usr_hs.pkl'), 'wb') as doc:
            pkl.dump(self.usr_hs, doc)
        with open(os.path.join(users_dir_path,  'usr_hobby.pkl'), 'wb') as doc:
            pkl.dump(self.usr_hobby, doc)

    def change_usr_pd(self,usr_pd):
        self.usr_pd=usr_pd
    def change_usr_hs(self,usr_hs):
        self.usr_hs=usr_hs
    def change_usr_hobby(self,usr_hobby):
        self.usr_hobby=usr_hobby
    def change_usr(self,usr):
        self.user=usr

    def get_usr_pd(self):
        return self.usr_pd
    def get_usr_hs(self):
        return self.usr_hs
    def get_usr_hobby(self):
        return self.usr_hobby
    def get_usr(self):
        return self.user

    def login_judge(self,username,pd):
        if username in list(self.usr_pd.keys()):
            if pd == self.usr_pd[username]:
                return True
        return False


if __name__=="__main__":
    g=UserUnit()
    g.save()