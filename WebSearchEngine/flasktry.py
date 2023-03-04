from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
import queryUnit
import UserUnit




app = Flask(__name__)


# usr_pd={}
# usr_pd['1']="1"

global_user=UserUnit.UserUnit()
global_user.load()
query_unit=queryUnit.Query()
# global_user_name='root'
usr_pd = {}
usr_hobby = {}
usr_hs = {}


'''
{% if page_num == page_of_blogs.number %}
    <li class="active">
        <span>{{ page_num }}</span>
    </li>
{% else %}
    <li>
        <a href="?page={{ page_num }}">{{ page_num }}</a>
    </li>
{% endif %}
'''
'''
@app.route('/',methods=['POST','GET'])
def result():
    p1=['http://cc.nankai.edu.cn/13256/list.htm','学院概况','fgtftydytrdtdty']
    p2 = ['http://cc.nankai.edu.cn/13256/list.htm', '学院概sdfdsf', 'fgtftydy888888888888888trdtdty']
    page=[]
    page.append(p1)
    page.append(p2)


    return render_template('result.html',page_list=page)

'''

# @app.route('/')
# def start():
#     return render_template('login.html')

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
   # return  render_template('source_code/0.html')




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





   #return render_template('advanced_search.html')



# 高级搜索返回常规搜索
@app.route('/return_to_common_search')
def return_to_common_search():
   return render_template('search.html')




'''
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

'''
if __name__ == '__main__':
   app.run()
