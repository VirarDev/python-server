import os
import uuid

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = get_table_name()

import functions.sql.basics
from functions.chat import mail
import random

get = lambda body:functions.sql.basics.get(TABLE_NAME,body)
count = lambda body:functions.sql.basics.count(TABLE_NAME,body)
store = lambda body:functions.sql.basics.store(TABLE_NAME,body)
update = lambda body:functions.sql.basics.update(TABLE_NAME,body)
delete = lambda body:functions.sql.basics.delete(TABLE_NAME,body)
run = lambda body:functions.sql.basics.run(TABLE_NAME,body)
def get_columns():return functions.sql.basics.get_columns(TABLE_NAME)
def pragma():return functions.sql.basics.pragma(TABLE_NAME)


def create_account(body):
    DeveloperKey = body["DevKey"]
    if(DeveloperKey == "Jayaraj@87"):
        pass
    else:
        return functions.sql.basics.js({
            "status":"success"
        })
    
    try:
        user_name = body["USER_NAME"]
        Pass = body["PASSWORD"]
        
        ID = str(uuid.uuid4())

        resp = functions.sql.basics.store(TABLE_NAME,{
            "ID" : ID,
            "DATA" : {
                "USER_NAME" : user_name,
                "PassWord" : Pass
            }
        })

        return resp

    except Exception as e:
        return "Error : "+str(e)

def delete_account(body):
    DeveloperKey = body["DevKey"]
    if(DeveloperKey == "Jayaraj@87"):
        pass
    else:
        return functions.sql.basics.js({
            "status":"success"
        })
    
    try:
        user_name = body["USER_NAME"]
        # Pass = body["PASSWORD"]
        
        resp = functions.sql.basics.delete(TABLE_NAME,{
            "CONDITION": f"USER_NAME = '{user_name}'"
        })

        return str(resp)

    except Exception as e:
        return "Error : "+str(e)


def auth_sign_in(body):
    try:
        user_name = body["USER_NAME"]
        Pass = body["PASSWORD"]

        #Id text primary key,USER_NAME text,PassWord text

        Users = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS": "password,id,user_name",
            "CONDITION": f"WHERE user_name = '{user_name}'"
        },True)

        columns = Users[0]
        Users = Users[1:]

        if(len(Users) == 0):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"User Name Not Found"
            })
        
        Found = False
        userDetail = None
        for user in Users:
            if(user[0] == Pass):
                Found = True
                userDetail = user
                break
        
        if(Found == False):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Incorrect Password"
            })
        
        userDetailDict = {}
        for i in range(len(columns)):
            detail = userDetail[i]
            column = columns[i]
            userDetailDict[column] = detail
        

        token = functions.sql.basics.getTokenForData(userDetailDict)

        return functions.sql.basics.js({
            "status":"success",
            "token":token
        })
    
    except Exception as e:
        return "Error : "+str(e)
