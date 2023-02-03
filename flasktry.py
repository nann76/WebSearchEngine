from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
import queryUnit
import UserUnit



app = Flask(__name__)


# usr_pd={}
# usr_pd['1']="1"

global_user=UserUnit.UserUnit()
global_user.load()

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
    # return render_template('login.html')
    return render_template('search.html')


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


# 常规搜索
@app.route('/common_search',methods=['POST'])
def common_search():
   input_sr=request.form['input_search']
   print(input_sr)

# 高级搜索
@app.route('/turn_to_advanced_search')
def turn_to_advanced_search():
   print('222')
   return render_template('advanced_search.html')


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
