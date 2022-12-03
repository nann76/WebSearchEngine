from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
app = Flask(__name__)


usr_pd={}
usr_pd['1']="1"


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/judge',methods=['POST'])
def judge():
   user = request.form['nm']
   password= request.form['pd']

   if user in list(usr_pd.keys()):
         if password==usr_pd[user]:
            return "login in"

   #return "login false"
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
