import requests
import re
import os
from bs4 import BeautifulSoup
from IdMap import IdMap
import pandas as pd
import pickle as pkl


def get_html(url):
    # print("try to get: ", url)
    try:
        temp =requests.get(url, timeout=2)
        temp.encoding = 'utf-8'
    except:
        return None
    return temp



base_url = 'http://cc.nankai.edu.cn'
dir_path = "C:/Users/nan/Desktop/Web_Search_Engine/data/"
url_id_map = IdMap()  # url to id

url_archor_list=[]      #url和锚文本的列表
url_title_list=[]       #url和title的列表
url_linkto={}           #url的link


url_list=[] #url的栈
url_done=[] #已经探索过的url
url_list.append(base_url)
max_loop = 100

def spider():
    cur_loop=0
    while cur_loop<max_loop and len(url_list)!=0:
        cur=url_list[0]
        print("cur_loop",cur_loop)
        #防止重复探索一个url
        if cur in url_done:
            url_list.remove(cur)
            continue
        print("cur ；  ",cur)
        #r = get_html(cur)
        r=get_html(cur)
        if r==None:
            url_list.remove(cur)
            continue
        if r.status_code!=200:
            url_list.remove(cur)
            continue

        soup = BeautifulSoup(r.text, "lxml")

        url_id=url_id_map[cur]
        #source code
        doc=open(os.path.join(dir_path,'source_code/'+str(url_id)+'.html'),'w',encoding='utf-8')
        doc.write(r.text)
        doc.close()

        #add title_url
        try:
            title = soup.find('title').text
            print(title)
            url_title_list.append([title,cur])
            print(url_title_list)
        except :
            url_list.remove(cur)
            continue


        #content
        data_list = soup.select('head')
        content=''
        for item in data_list:
            text=re.sub('[\r \n\t]', '', item.get_text())
            text = re.sub('[\s]', '', text)
            if text==None or text=='':
                continue
            content+=text
        data_list = soup.select('body')
        for item in data_list:
            text=re.sub('[\r \n\t]', '', item.get_text())
            text = re.sub('[\s]', '', text)
            if text==None or text=='':
                continue
            #print(text)
            content += text
            #print(content)

        #remove
        if os.path.exists(os.path.join(dir_path, 'content/' + str(url_id) + '.txt')):
            os.remove(os.path.join(dir_path, 'content/' + str(url_id) + '.txt'))
            print('remove sucessful')
        else:
            print("not exits")

        with open(os.path.join(dir_path, 'content/' + str(url_id) + '.txt'), 'w',encoding='utf-8') as doc:
            doc.write(content)


        data_list= soup.find_all('a')
        #print(title_list.text)
        linkto=[]
        for item in data_list:
            #锚文本
            archor = item.text.strip().replace(' ','').replace('\n','').replace('\t','')
            #链接url
            str_url = str(item.get('href'))
            #print(str_url)
            if "http" in str_url:

                url_archor_list.append([archor, str_url])
                url_list.append(str_url)
                temp_url_id=url_id_map[str_url]
                linkto.append(temp_url_id)

            elif "htm" in str_url :

                com_str=str(base_url + str_url)
                url_archor_list.append([archor, com_str])
                url_list.append(com_str)
                temp_url_id=url_id_map[com_str]
                linkto.append(temp_url_id)

        url_done.append(cur)
        url_linkto[url_id_map[cur]]=linkto
        #print(len(url_linkto))
        #print(url_linkto)
        #print(url_list)
        url_list.remove(cur)
        cur_loop+=1






def save():
    ############################archor_url##############################
    # remove
    if os.path.exists(os.path.join(dir_path, 'archor_url.csv')):
        os.remove(os.path.join(dir_path, 'archor_url.csv'))
        print('remove sucessful')
    else:
        print("not exits")

    # save archor_url
    df1 = pd.DataFrame(data=url_archor_list, columns=["archor", "url"])
    df1.to_csv(os.path.join(dir_path, 'archor_url.csv'), encoding='utf_8_sig')
    ###################################################################

    #############################title_url#############################
    # remove
    if os.path.exists(os.path.join(dir_path, 'title_url.csv')):
        os.remove(os.path.join(dir_path, 'title_url.csv'))
        print('remove sucessful')
    else:
        print("not exits")

    # save archor_url
    df1 = pd.DataFrame(data=url_title_list, columns=["title", "url"])
    df1.to_csv(os.path.join(dir_path, 'title_url.csv'), encoding='utf_8_sig')
    ###################################################################

    #序列化
    try:
        os.mkdir(os.path.join(dir_path, "pkl_dir"))
    except FileExistsError:
        pass
    #url_id_map
    with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'wb') as doc:
        pkl.dump(url_id_map, doc)

    #url_linkto_dict
    with open(os.path.join(dir_path, "pkl_dir/" + "url_linkto_dict.pkl"), 'wb') as doc:
        pkl.dump(url_linkto, doc)
'''
###################################################################
    # remove
    if os.path.exists(os.path.join(dir_path, 'url_linkto.csv')):
        os.remove(os.path.join(dir_path, 'url_linkto.csv'))
        print('remove sucessful')
    else:
        print("not exits")

    # df1=pd.DataFrame(data=url_linkto,columns=["url","linkto_url"])
    # df1.to_csv(os.path.join(dir_path, 'url_linkto.csv'),encoding='utf-8')


###################################################################
'''


def load():

    with open(os.path.join(dir_path, "pkl_dir/" + 'url_id_map.pkl'), 'rb') as doc:
        url_id_map = pkl.load(doc)

    with open(os.path.join(dir_path, "pkl_dir/" + "url_linkto_dict.pkl"), 'rb') as doc:
        url_linkto=pkl.load(doc)


if __name__ == "__main__":


    spider()
    save()


