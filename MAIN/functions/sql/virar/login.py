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


def send_otp_for_register(body):
    try:
        Email = body["EMAIL"]
        # Otp = 123456
        random_code = ''.join(random.choices('0123456789', k=6))
        Otp = int(random_code)

        Users = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS": "password,id,email,name,phone,lastloginepoch",
            "CONDITION": f"WHERE email = '{Email}'"
        },True)[1:]

        if(len(Users) != 0):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Email Address Already Found"
            })

        token = functions.sql.basics.getTokenForData({
            "email":Email,
            "otp":Otp
        })

        mail({
            "MAIL_TO":Email,
            "SUBJECT":"OTP From Virar Gaming YT",
            "BODY":"Your OTP (One TIme Password) is : "+str(Otp)
        })

        return functions.sql.basics.js({
            "status":"success",
            "token":token
        })
    except Exception as e:
        return "Error : "+str(e)

def verify_otp_for_register(body):
    try:
        token = body["TOKEN"]
        email = body["EMAIL"]
        otp = body["OTP"]

        Phone = body["PHONE"]
        Name = body["NAME"]
        Password = body["PASSWORD"]

        Data = functions.sql.basics.getDataForToken(token)
        if(Data["status"] == "expired"):
            return functions.sql.basics.js({
                "status":"sto"
            })
        
        Data = Data["data"]

        if(Data["email"] != email or Data["otp"] != otp):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Invalid OTP"
            })
        
        newToken = functions.sql.basics.getTokenForData({
            "email":email
        })


        return auth_sign_up({
            "TOKEN":newToken,
            "PHONE" : Phone,
            "NAME" : Name,
            "PASSWORD" : Password
        })
        
        return functions.sql.basics.js({
            "status":"success",
            "message":"OTP Verified",
            "token":newToken
        })

    except Exception as e:
        return "Error : "+str(e)

def auth_sign_up(body):
    try:
        Token = body["TOKEN"]
        Phone = body["PHONE"]
        Name = body["NAME"]
        Password = body["PASSWORD"]

        Data = functions.sql.basics.getDataForToken(Token)
        
        if(Data["status"] == "expired"):
            return functions.sql.basics.js({
                "status":"sto"
            })
        
        Data = Data["data"]
        Email = Data["email"]

        res = functions.sql.basics.store("login",{
            "ID":Email,
            "DATA":{
                "lastloginepoch":functions.sql.basics.get_current_epoch_time(),
                "email":Email,
                "name":Name,
                "phone":Phone,
                "password":Password
            }
        })
        if("duplicate key" in res):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Email Already Registered",
            })

        if(res != "ok"):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Try Again Please",
            })
        
        return auth_sign_in({
            "EMAIL":Email,
            "PASSWORD":Password
        })

    except Exception as e:
        return "Error : "+str(e)


def auth_sign_in(body):
    try:
        Email = body["EMAIL"]
        Pass = body["PASSWORD"]

        Users = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS": "password,id,email,name,phone,lastloginepoch",
            "CONDITION": f"WHERE email = '{Email}'"
        },True)

        columns = Users[0]
        Users = Users[1:]

        if(len(Users) == 0):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"Email Address Not Found"
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
            "token":token,
            "details":{
                "Email":Email,
                "Name":userDetailDict["name"],
                "Phone":userDetailDict["phone"]
            }
        })
    except Exception as e:
        return "Error : "+str(e)
