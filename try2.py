from flask import Flask, redirect, url_for, request,render_template
from flask import render_template
app = Flask(__name__)

user = '1'
password = '1'
usr_pd={}
usr_pd['1']="1"
print(usr_pd)

print(list(usr_pd.keys()))
print(str(usr_pd['1']))
if user in list((usr_pd.keys())):
    print("1111")
    if password == usr_pd[user]:
        print('2222')
