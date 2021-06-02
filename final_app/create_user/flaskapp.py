from flask import Flask, request, render_template,jsonify
from werkzeug.exceptions import RequestEntityTooLarge
import publisher
import pymongo
import json
import sys
import bcrypt
import os
import database

#Flask Part
app = Flask(__name__)
data = {"key":"this is default"}

#The Dockerfile will execute flaskapp with the host IP defined
host_ip = sys.argv[1]
#host_ip = "127.0.0.1"
#define the database address so that we could call it whenever we need to connect to the database
db_add = "mongodb://"+host_ip+":27017/"

#this variable is for connection testing only
test_message={}

#database part, define database name, collection, etc for mongodb
myclient = pymongo.MongoClient(db_add)
mydb = myclient["mydatabase"]
mycol = mydb["key"]

@app.route('/register',methods=['GET'])
def entry_point():
    error_msg=""
    return render_template('index.html', error_msg=error_msg)

@app.route('/insert',methods=['POST'])
def insert_db():
    #data = request.get_json() #this part is fecth the value from the request body
    
    #check if the password and re-enter password is NOT match 
    if request.form['psw'] != request.form['psw-repeat']:
        error_msg="Password did not Match"
        return render_template('index.html', error_msg=error_msg)
    else:
        #get the value from the html form 
        fname = request.form['fname']
        lname = request.form['lname']
        uname = request.form['uname']
        email = request.form['email']
        psw = request.form['psw']
        message = {
            "fname": fname,
            "lname": lname,
            "uname": uname,
            "email": email,
            "psw": bcrypt.hashpw(psw.encode(), bcrypt.gensalt()).decode('utf-8'),
        }
        
        #this variable for checking connection only
        global test_message
        test_message = message

        #check if the uname already exist
        data_ = database.main(db_add)
        user = list(filter(lambda user: user['uname'] == uname, data_))
        if len(user) != 0:
            error_msg = "The username already exist"
            return render_template('index.html', error_msg=error_msg)
        else:
            #send the message to the publisher 
            publisher.publisher(json.dumps(message), host_ip)
            error_msg="New Record Added!"
            return render_template('index.html', error_msg=error_msg)

#this is for testting only
@app.route('/test',methods=['GET'])
def check():
    if request.args.get('psw') is None:
        global test_message
        return test_message
    else:
        #use this to check whether or not Inputted password match with database
        new_psw = request.args.get('psw')
        check = bcrypt.checkpw(new_psw.encode(), test_message['psw'].encode('utf-8'))
        return str(check)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    

