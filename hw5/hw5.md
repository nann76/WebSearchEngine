<h1 align = "center">信息系统检索</h1>

<center><font size='5'><b>HW5 Web搜素引擎</b></font>     </center>

<center><b>姓名： 蒋浩南      &emsp;&emsp;  学号：2012948 </b>    </center>

[toc]

### 一、网页抓取

​	功能实现：

1. 从`base_url`开始。
   * 每次访问网页，将该网页的源代码（html文件）保存到本地，为之后实现网页快照功能。
   * 提取该网页的content，保存到本地。
   * 提取该网页的title，加入`url_title_list`，url和title的列表。
   * 提取该网页的锚文本，并将对应的url，加入`url_archor_list`。同时将url加入到探索的url栈中，以继续探索。以及设置该网页指向的网页信息（url_linkto），为之后PageRank提供数据。（使用IdMap()实现对url的数字对应）

```python

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
        url_list.remove(cur)
        cur_loop+=1

```

2. 保存

对爬取过程中的数据进行保存。

```python
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
```



### 二、文本索引

文本索引的构建分为两部分：

* 第一部分使用`whoosh`,分别对Title、锚文本、url和网页的总内容建立索引。由于直接通过爬取的原始数据构建索引，在后面实现短语查询。
* 第二部分为通过`TfidfVectorizer`对不同域建立向量空间模型。实现其他的查询功能。



1. 如下为第一部分，使用`whoosh`建立索引并保存至本地。使用第一部分使用爬虫爬取的数据。以下四个函数分别为对title、锚文本、url和content建立索引的函数。基本相同，都是读取对应数据，创建索引结构，对原数据进行一定的处理后，加入索引中。

```python
def build_Title_Index():

    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    title_url=read_csv(dir_path+'/'+'title_url.csv')
    title_url=title_url.values.tolist()

    schema = Schema(url=NUMERIC(stored=True), title=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_title_source')
    writer = ix.writer()

    for term in title_url:

        if term[1] != '':
           url_temp=id_map[term[2]]
           title_temp=str(term[1])
           title_temp = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", title_temp)
           title_temp = title_temp.lower()
           #words = ' '.join(jieba.lcut_for_search(title_temp))
           writer.add_document(url=url_temp, title=title_temp )
    writer.commit()

def build_Archor_Index():

    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    archor_url=read_csv(dir_path+'/'+'archor_url.csv')
    archor_url=archor_url.values.tolist()

    schema = Schema(url=NUMERIC(stored=True), archor=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_archor_source')
    writer = ix.writer()

    for term in archor_url:
            #term = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", term)
            if  term[1]!='':
                url_temp = id_map[term[2]]
                archor_temp = str(term[1])
                archor_temp = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", archor_temp)
                archor_temp = archor_temp.lower()
                #words = ' '.join(jieba.lcut_for_search(archor_temp))
                print(id_map[term[2]],term[1])
                writer.add_document(url=url_temp, archor=archor_temp )
    writer.commit()

def build_Url_Index():

    id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')
    # archor_url=read_csv(dir_path+'/'+'archor_url.csv')
    # archor_url=archor_url.values.tolist()

    # schema = Schema(url=NUMERIC(stored=True), archor=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构
    schema = Schema(url=NUMERIC(stored=True), url_text=TEXT(stored=True))  # 创建索引结构


    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_source')
    writer = ix.writer()

    for term in (id_map.str_to_id).keys():
            # print(id_map[term],term)
            writer.add_document(url=id_map[term], url_text=term )
    writer.commit()

def build_Content_Index():

    #id_map=read_IdMap(dir_pkl_path+'/'+'url_id_map.pkl')


    schema = Schema(url=NUMERIC(stored=True), content=TEXT(stored=True, analyzer=ChineseAnalyzer()))  # 创建索引结构

    ix = create_in(os.path.join(dir_index_path), schema=schema, indexname='url_content_source')
    writer = ix.writer()

    max_doc = 108
    temp_doc=0
    while temp_doc<max_doc:
        doc=str(temp_doc)+'.txt'
        print(dir_content_path + '/'+doc)
        doc_dir=dir_content_path + '/' + doc

        term=''
        try:
            for content in open(dir_content_path + '/' + doc, encoding='utf-8').readlines():
                # print(content)
                content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", content)
                content = content.lower()
                term=term+content
            writer.add_document(url=temp_doc, content=term)
            temp_doc+=1
        except:
            temp_doc+=1
            continue

    writer.commit()

```

2. 如下为第二部分，使用`TfidfVectorizer`对不同域建立向量空间模型。

* 实现思路都为首先对原始的数据进行处理（如去掉中文符号，最小化），生成每个url（网页）对于的list，之后组合形成`doc_list`。建立`tfidf_vectorizer = TfidfVectorizer(min_df=1)`,之后`tfidf_matrix =tfidf_vectorizer.fit_transform(doc_list)`得到`tfidf_vectorizer `为之后生成查询向量。  `tfidf_matrix `为tfidf矩阵，为之后计算分数。`tfidf_vectorizer.get_feature_names_out()`为词袋，为之后通配查询时匹配用。序列化保存。

```python
def genContentVSM():
    doc_list = []
    url_list = []
    temp_doc=0

    while temp_doc<max_doc:
        doc=str(temp_doc)+'.txt'
        print(dir_content_path + '/'+doc)

        try:
            for content in open(dir_content_path + '/' + doc, encoding='utf-8').readlines():
                content = re.sub(r"[{}、，。！？·【】）》；;—《“”：（-]+".format(punctuation), "", content)
                content = content.lower()
                words = ' '.join(jieba.lcut_for_search(content))
                doc_list.append(words)
        except:
            content = ' '
            words = ' '.join(jieba.lcut_for_search(content))
            doc_list.append(words)
            temp_doc += 1
            url_list.append(doc[0:-4])
            continue
        temp_doc+=1


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



```




### 三、链接分析

* 使用包`import networkx as nx`
* 读取网页爬取时保存的`url_linkto`
* ` G=nx.DiGraph()`加边
* `pr = nx.pagerank(G, alpha=0.85)`得到pageRank的矩阵
* 序列化保存，作为之后搜索排序时网页得分的一部分。

```python
def pageRank():
    url_linkto=read_url_linkto()
    G=nx.DiGraph()
    #加边
    for i in url_linkto:
            for j in url_linkto[i]:
                G.add_edge(i,j)
    #计算，阻尼因子 0.85
    pr = nx.pagerank(G, alpha=0.85)
    print(pr)
    prdic = {}
    for node, pageRankValue in pr.items():
            prdic[node] = pageRankValue * 1e4
    print(prdic)

    #序列化
    with open(os.path.join(dir_pkl_path , 'pageRRank.pkl'), 'wb') as doc:
        pkl.dump(prdic, doc)

```

### 四、查询服务









### 五、个性化查询

函数输入为：

* qr：为查询返回的字典，其key为url（使用IdMap（），即url对于的数字）。values为前面计算得到的分数。
* hobby：为用户在注册时选择的兴趣标签。
* history：为用户的查询历史。

实现思路：

* 利用查询分别对hobby和history做查询，得到对应的查询结果字典。
* 如果hobby和history中的key也存在于输入的字典中，则对输入的字典中该key对应的分数有加分，即`qr[key]+=url_score_hobby[key]/para_hobby`。

* 实现的效果为对含有兴趣标签和查询历史特征的网页有一定加分。

```python
    #个性化查询,为不同的⽤户提供不同的内容排序
    def add_personal_queries(self,qr,hobby=None,history=None,para_hobby=10,para_history=20):

        str_hobby=''
        for i in hobby:
            str_hobby+=i+' '
        str_history=''
        for i in history:
            str_history+=i+' '

        # print(str_hobby)
        # print(str_history)
        url_score_hobby=Query.common_query(self,str_hobby)
        url_score_history=Query.common_query(self,str_history)
        # print(url_score_hobby)
        # print(url_score_history)

        qr_keys=qr.keys()
        url_score_hobby_keys=url_score_hobby.keys()
        url_score_history_keys=url_score_history.keys()

        for key in url_score_hobby_keys:
            if key in qr_keys:
                qr[key]+=url_score_hobby[key]/para_hobby


        for key in url_score_history_keys:
            if key in qr_keys:
                qr[key]+=url_score_history[key]/para_history
```



### 六、个性化推荐

​		该部分使用`synonyms`包，生成输入的hobby和history（兴趣标签和查询历史）的近义词列表。利用近义词列表进行查询，得到推荐的网页字典。与输入的未经过推荐查询的字典结合，做set。得到个性化推荐后的查询字典。

函数输入为：

* qr：为查询返回的字典其key为url（使用IdMap（），即url对于的数字）。values为前面计算得到的分数。
* hobby：为用户在注册时选择的兴趣标签。
* history：为用户的查询历史。

实现思路：

* 对输入的hobby和history进行预处理。生成近义词列表，得到符合查询的输入。
* 利用查询分别对hobby和history做查询，得到对应的查询结果字典。
* 与输入的未经过推荐查询的字典结合，做set。得到个性化推荐后的查询字典。
* 返回结合后的查询字典(经过个性化推荐，有所扩充)

```python
   # 个性化推荐
    def add_personal_recommendation(self ,qr,hobby=None,history=None):

        print('start personal_recommendation')

        #根据爱好标签
        rec_hobby=[]
        for h in hobby:
            # hh=synonyms.display(h,size=3)
            rec_hobby.extend(synonyms.nearby(h,size=5)[0])
        print('rec hobby',rec_hobby)

        # 根据查询历史
        r_history=list(reversed(history))
        if len(r_history)>5:
            r_history=r_history[0:5]
        rec_history = []
        for hh in r_history:
            h = jieba.lcut(hh)
            for _ in h:
                rec_history.extend(synonyms.nearby(_, size=3)[0])
        print('rec history', rec_history)

        st_hobby=''

        for temp in rec_hobby:
            st_hobby+=temp+' '
        st_history=''
        for temp in rec_history:
            st_history+=temp+' '
        # 推荐内容的查询
        url_score_hobby=Query.common_query(self,st_hobby)
        url_score_history=Query.common_query(self,st_history)

        after_add_personal_recommendation = dict(qr)

        for i in url_score_hobby.keys():
            url_score_hobby[i] = url_score_hobby[i] / 10
        for i in url_score_history.keys():
            url_score_history[i] = url_score_history[i] / 50

        after_add_personal_recommendation.update(url_score_hobby)
        after_add_personal_recommendation.update(url_score_history)
        set(after_add_personal_recommendation)
        print(after_add_personal_recommendation)
        print('end personal_recommendation')
        return  after_add_personal_recommendation
```



### 七、Web页面，图形化界面

网页分为以下部分：

* 开始的是登入页面，可以选择登入或者注册。
* 注册页面：进行注册，注册后转到兴趣选择页面。
* 兴趣选择页面：选择感兴趣的标签。提交后转回到登入页面。
* 常规搜索页面：进行站内查询，查询范围为网页的全部内容。左上角高级搜索和查询历史。
* 查询历史：可以显示当前登录用户的查询历史。
* 高级搜索：可以进行供站内查询、短语查询、通配查询。可以选择查询得范围。以及设置站内查询地址。
* 查询结果界面：现实查询结果。点击标题跳转，显示部分网页内容。网页快照按钮可以打开本地存储的对应网页。



代码实现：

使用`flask`框架编写。

```python
from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
import queryUnit
import UserUnit

app = Flask(__name__)

global_user=UserUnit.UserUnit()
global_user.load()
query_unit=queryUnit.Query()
# global_user_name='root'
usr_pd = {}
usr_hobby = {}
usr_hs = {}


#开始
@app.route('/')
def start():
    return render_template('login.html')
    # return render_template('advanced_search.html')
    # return render_template('search.html')


# 跳转至注册
@app.route('/turn_to_register',methods=['POST'])
def turn_to_register():
   return render_template('register.html')

# 注册
@app.route('/register',methods=['POST'])
def register():

   user = request.form['nm']
   password= request.form['pd']

   print((user,password))

   global_user.user=user
   usr_pd[user]=password
   global_user.change_usr_pd(usr_pd)

   print(global_user.usr_pd)
   return render_template('choose.html')


# 选择爱好标签
@app.route('/choose',methods=['POST'])
def choose():
   joy = request.form.getlist('cb')
   print(joy)
   usr_hobby[global_user.user]=joy
   global_user.change_usr_hobby(usr_hobby)
   print(global_user.usr_hobby)
   global_user.save()

   return render_template('login.html')

#登入
@app.route('/login',methods=['POST'])
def login():
   username = request.form['nm']
   password= request.form['pd']

   if global_user.login_judge(username,password):
      global_user.user=username
      return render_template('search.html')
   #return "login false"
   return render_template('login.html')

#网页快照跳转
@app.route('/turn_to_web_page_snapshot',methods=['POST','GET'])
def turn_to_web_page_snapshot():
   id = request.args.get('id')
   print(id)
   st='source_code/'+str(id)+'.html'
   print(st)
   return  render_template(st)



# 常规站内搜索
@app.route('/common_search',methods=['POST'])
def common_search():
   input_sr=request.form['input_search']
   print(input_sr)
   if input_sr!='':
      usr_hs= global_user.get_usr_hs()
      if global_user.user not in usr_hs.keys():
         list=[]
         list.append(input_sr)
         usr_hs[global_user.user]=list
      else:
         usr_hs[global_user.user].append(input_sr)
   global_user.change_usr_hs(usr_hs)
   global_user.save()

   # global_user.user = '1'
   usr_hobby = global_user.get_usr_hobby()
   hobby = usr_hobby[global_user.user]
   print(hobby)
   history = global_user.get_usr_hs()
   history = history[global_user.user]
   print(history)
   page=query_unit.query(input_query=input_sr,query_type=3,hobby=hobby,history=history)

   # print(page)
   print(global_user.usr_hs[global_user.user])

   return  render_template('result.html', page_list=page)


# 转到查询日志
@app.route('/turn_to_search_log',methods=['POST','GET'])
def turn_to_search_log():
   # print('111')
   search_log=global_user.get_usr_hs()
   search_log=search_log[global_user.get_usr()]
   search_log=reversed(search_log)
   return render_template('search_log.html',page_list=search_log)



# 转到高级搜索
@app.route('/turn_to_advanced_search')
def turn_to_advanced_search():
   # print('222')
   return render_template('advanced_search.html')


# 高级搜索
@app.route('/advanced_search',methods=['POST' ])
def advanced_search():

   phrase=request.form['q1']
   wildcard = request.form['q2']
   inside_station = request.form['q3']
   # q4 = request.form['q4']
   q5 = request.form.get('q5')
   q6 = request.form['q6']


   query=''
   query_type=0
   if phrase!='' and wildcard=='' and inside_station=='':
      query=phrase
      query_type=1
   elif phrase == '' and wildcard != '' and inside_station == '':
      query = wildcard
      query_type=2
   elif phrase == '' and wildcard == '' and inside_station != '':
      query=inside_station
      query_type=3



   position_type=0
   if q5=='0':
      position_type=0
   if q5=='1':
      position_type=1
   if q5=='2':
      position_type=2
   if q5=='3':
      position_type=3


   print(phrase)
   print(wildcard)
   print(inside_station)
   # print(q4)
   print(q5)
   print(q6)
   print(query)
   print(query_type)
   print(position_type)

   # global_user.user='1'
   usr_hobby=global_user.get_usr_hobby()
   hobby=usr_hobby[global_user.user]
   print(hobby)
   history=global_user.get_usr_hs()
   history=history[global_user.user]
   print(history)
   page=query_unit.query(input_query=query,query_type=query_type,positin_type=position_type,hobby=hobby,history=history)
   print(page)

   return  render_template('result.html', page_list=page)


# 高级搜索返回常规搜索
@app.route('/return_to_common_search')
def return_to_common_search():
   return render_template('search.html')


if __name__ == '__main__':
   app.run()

```





