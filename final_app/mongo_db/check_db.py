import pymongo
import sys
import json

#host=ip:port
host_ip = sys.argv[1]

#database part
db_add = "mongodb://"+host_ip+"/"
myclient = pymongo.MongoClient(db_add)
mydb = myclient["mydatabase"]
mycol = mydb = mydb["key"]

def db_all():
    db_list = []
    for x in mycol.find():
        data = str(x).replace("ObjectId(","")
        data = data.replace(")","")
        data = data.replace("'",'"')
        #db_list.append(json.loads(data))
        print(json.loads(data))
    return "DONE"

if __name__ == '__main__':
    print(db_all())
