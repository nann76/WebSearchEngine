from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
app = Flask(__name__)


usr_pd={}
usr_pd['1']="1"


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

@app.route('/')
def start():
    return render_template('login.html')



@app.route('/login',methods=['POST'])
def judge():
   user = request.form['nm']
   password= request.form['pd']

   if user in list(usr_pd.keys()):
         if password==usr_pd[user]:
            # return "login in"
            return render_template('search.html')
   #return "login false"
   return render_template('login.html')


@app.route('/turn_to_register',methods=['POST'])
def turn_to_register():
   return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():

   user = request.form['nm']
   password= request.form['pd']

   print((user,password))
   return render_template('login.html')



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
