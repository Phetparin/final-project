from flask import Flask, request, jsonify, render_template,g , session, url_for, redirect
import pymongo
import json
import database
import sys
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'youknowwhat?Imsmartthanyouknow'
host_ip = sys.argv[1]
#host_ip = "127.0.0.1"
db_add = "mongodb://"+host_ip+":27018/"
db_add_del = "mongodb://"+host_ip+":27017/"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.String(200), nullable=True)
    pic = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    uname = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return '<Task %r>' % self.id 

db.create_all()

def load_db(_key, _value):
    data_ = database.main(db_add)
    user = list(filter(lambda user: user[_key] == _value, data_))
    return user

@app.before_request
def load_user():
    g.user = None
    if 'user_id' in session:
        data_ = database.main(db_add)
        user = load_db('_id', session['user_id'])
        try:
            g.user = user[0]
        except:
            g.user =None

@app.route('/', methods=[ 'GET','POST'])
def main():
    if request.method == 'POST':
        data_ = database.main(db_add)
        uname = request.form['uname']
        psw = request.form['psw']
        user = load_db('uname', uname)
        
        #session
        session.pop('user_id', None)
        try:
            if bcrypt.checkpw(psw.encode(), user[0]['psw'].encode('utf-8')):
                user_id = user[0]['_id']
                session['user_id'] = user_id
                g._id = user_id
                return redirect(url_for('todo'))
            else:
                return render_template('login.html', alert="Wrong User/ Password")
        except:
            return render_template('login.html', alert="Invalid User")
    else:
        return render_template('login.html', alert="")
    
@app.route('/listuser',methods=['GET'])
def listuser():
    if not g.user:
        return "Prohibited"
    if g.user['uname'] == "admin":
        data_ = database.main(db_add)
        return render_template('listuser.html', data_= data_)
    else: 
        return redirect(url_for('todo'))

#todo
@app.route('/todo',methods=['GET', 'POST'])
def todo():
    if not g.user:
        return "Prohibited"

    uname = g.user['uname']
    if request.method == 'POST':
        task_content = request.form['content']
        task_deadline = request.form['deadline']
        task_pic = request.form['pic']
        task_uname = uname
        new_task = Todo(content=task_content, deadline=task_deadline, pic=task_pic, uname=task_uname )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue'
 
    else:
        tasks = Todo.query.order_by(Todo.date_created).filter(Todo.uname == uname).all()
        return render_template('todo.html', tasks=tasks)  

@app.route('/delete/<int:id>')
def delete(id):
    if not g.user:
        return "Prohibited"
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
            return 'There was an issue with deleting that task'

@app.route('/mongodel')
def mongodel():
    if not g.user:
        return "Prohibited"
    uname= json.loads(request.args.get('user').replace("'",'"'))
    uname.pop('_id')
    delete_ = database.delete(db_add_del, uname)
    return redirect('/listuser')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if not g.user:
        return "Prohibited"
    task_to_update = Todo.query.get_or_404(id)
   
    if request.method == 'POST':   
        task_to_update.content = request.form['content']
        task_to_update.deadline = request.form['deadline']
        task_to_update.pic = request.form['pic']
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue with updating that task'
    else:
        return render_template('update.html', task=task_to_update)

@app.route('/logout', methods=['GET'])
def logout():
    g.user = None
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)
