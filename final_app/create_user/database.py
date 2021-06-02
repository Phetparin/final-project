import pymongo
import json

def db_all(mycol):
    db_list = []
    for x in mycol.find():
        data = str(x).replace("ObjectId(","")
        data = data.replace(")","")
        data = data.replace("'",'"')
        data = data.replace('"data": "{','')
        data = data.replace('}"','')
        db_list.append(json.loads(data))
    return db_list

def main(host_ip):
    #database part
    db_add = host_ip
    myclient = pymongo.MongoClient(db_add)
    mydb = myclient["mydatabase"]
    mycol = mydb["key"]
    return db_all(mycol)
    