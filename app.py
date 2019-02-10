from flask import Flask
from flask_bootstrap import Bootstrap
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
import logging
from sqlalchemy.orm import sessionmaker,scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
import win32api
from tabledef import *
engine = create_engine('sqlite:///kanban.db?check_same_thread=False', echo=True)
 
app = Flask(__name__)
bootstrap = Bootstrap(app)
Ses=sessionmaker(bind=engine)
@app.route('/')
def home(error=null):
    if not session.get('logged_in'):
        if error == null:
            return render_template('login.html')
        else:
            return render_template('login.html',error=error)
    else:
        return redirect(url_for('dashboard'))

def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['POST'])
def do_login():
    error=null
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    if POST_USERNAME!='' and POST_PASSWORD!='':
        s=Ses()
        query = s.query(User).filter(User.username.in_([POST_USERNAME]))
        result = query.first()
        if result:
            if check_password_hash(result.password,POST_PASSWORD):
                session['logged_in'] = True
                session['username']=POST_USERNAME
                return redirect(url_for('dashboard'))
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
            sa=Ses()
            query=sa.query(User).filter(User.username.in_([Get_Username]))
            result=query.first()
            if result:
                error='Username Already Exists!!'
                return showsignup(error)
            else:
                Hashed_Password=generate_password_hash(Get_Password, method='sha256')
                user = User(Get_Username,Hashed_Password)
                sa.add(user)
                sa.commit()
                session['logged_in'] = True
                session['username']=Get_Username
                return redirect(url_for('home'))
        else:
            error='Password does not match!!'
            return showsignup(error)
    else:
        error='Required Field Empty!!'
        return showsignup(error)      

@app.route("/showtask")
def showtask():
    if session['username']=='':
        return render_template('login.html')
    else:
        s=Ses()
        query=s.query(User).filter(User.username.in_([session['username']]))
        task_user=query.first()
        u_id=task_user.id
        return render_template('welcome.html',tasks=s.query(Task).filter(Task.u_id.in_([u_id])))

@app.route("/addtask",methods=['GET','POST'])
def add_task():
    s=Ses()
    query=s.query(User).filter(User.username.in_([session['username']]))
    task_user=query.first()
    u_id=task_user.id
    task_name=str(request.form['t_name'])
    task_desc=str(request.form['t_desc'])
    status=str(request.form['status'])
    new_task=Task(u_id,task_name,task_desc,status)
    s.add(new_task)
    s.commit()
    return redirect(url_for('dashboard'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    s=Ses()
    query=s.query(User).filter(User.username.in_([session['username']]))
    task_user=query.first()
    u_id=task_user.id
    todo = s.query(Task).filter(Task.status.in_(['Todo']),Task.u_id.in_([u_id]))
    doing = s.query(Task).filter(Task.status.in_(['doing']),Task.u_id.in_([u_id]))
    done = s.query(Task).filter(Task.status.in_(['done']),Task.u_id.in_([u_id]))
    return render_template('welcome.html', todo = todo, doing=doing, done=done)

@app.route('/doing/<t_id>', methods=['GET','POST'])
def doing(t_id):
    s=Ses()
    move_doing=s.query(Task).filter(Task.t_id.in_([int(t_id)])).first()
    move_doing.status ='doing'
    s.commit()
    return redirect(url_for('dashboard'))

@app.route('/done/<t_id>', methods=['GET','POST'])
def done(t_id):
    s=Ses()
    move_done = s.query(Task).filter(Task.t_id.in_([int(t_id)])).first()
    move_done.status ='done'
    s.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete/<t_id>', methods=['GET','POST'])
def delete(t_id):
    s=Ses()
    deleted = s.query(Task).filter(Task.t_id.in_([int(t_id)])).first()
    s.delete(deleted)
    s.commit()
    return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)