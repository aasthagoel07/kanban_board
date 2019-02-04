from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
import win32api
from tabledef import *
engine = create_engine('sqlite:///kanban.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home(error=null):
    if not session.get('logged_in'):
        if error == null:
            return render_template('login.html')
        else:
            return render_template('login.html',error=error)
    else:
        return "Hello!!"

def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['POST'])
def do_login():
    error=null
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    if POST_USERNAME!='' and POST_PASSWORD!='':
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]))
        result = query.first()
        if result:
            if check_password_hash(result.password,POST_PASSWORD):
                session['logged_in'] = True
                session['username']=POST_USERNAME
                return welcome()
            else:
                error= 'Wrong password!'
                return home(error)
        else:
            error='Username does not exist!!'
            return home(error)
    else:
        error='Required Fields Empty!'
        return home(error)

@app.route('/showsignup')
def showsignup(error=null):
    if error==null:
        return render_template('signup.html')
    else:
        return render_template('signup.html',error=error)

@app.route('/signup', methods=['POST'])
def do_signup():    
    error=None
    Get_Username=str(request.form['username'])
    Get_Password=str(request.form['password'])
    Get_CPassword=str(request.form['cpassword'])
    if Get_Username!='' and Get_Password!='' and Get_CPassword!='':
        if Get_Password==Get_CPassword:
            Session=sessionmaker(bind=engine)
            s=Session()
            query=s.query(User).filter(User.username.in_([Get_Username]))
            result=query.first()
            if result:
                error='Username Already Exists!!'
                return showsignup(error)
            else:
                Hashed_Password=generate_password_hash(Get_Password, method='sha256')
                user = User(username=Get_Username,password=Hashed_Password)
                s.add(user)
                s.commit()
                return redirect(url_for('home'))
        else:
            error='Password does not match!!'
            return showsignup(error)
    else:
        error='Required Field Empty!!'
        return showsignup(error)      
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home('Logged Out')
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)