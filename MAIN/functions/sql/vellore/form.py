import os
import uuid

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = get_table_name()

import functions.chat
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


def register(body):
    try:
        Details = body["DETAILS"]
        Email = body["EMAIL"]
        Name = Details["NAME"]

        resp = functions.sql.basics.count(TABLE_NAME,{
            "CONDITION": f"WHERE Email='{Email}'"
        },True)

        if(resp != 0):
            return functions.sql.basics.js({
                "status" : "fail",
                "message" : f"The e-mail '{Email}' is already registered, Try again with other email address"
            })
        
        Details["EMAIL"] = Email
        Details["RegisteredTime"] = functions.sql.basics.get_current_epoch_time()

        ID = str(uuid.uuid4())
        
        resp = functions.sql.basics.store(TABLE_NAME,{
            "ID" : ID,
            "DATA" : Details
        })

        BibNumber = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS": "bibnumber",
            "CONDITION": f"Where id = '{ID}'"
        },True)[1][0]

        BibNumber += 1000
        EmailBody = """
Helo {Name}, you registered for the event.
Here is your BIB Number : {BibNumber}
Do not miss it, Thank You For Registering!
""".format(Name=Name,BibNumber=BibNumber)
# Here is the link to see/view the Admit Card : 

        mail_resp = functions.chat.mail({
            "MAIL_TO" : Email,
            "SUBJECT" : "Vellore Archery Academy",
            "BODY" : EmailBody
        })

        return functions.sql.basics.js({
            "status":"success",
            "BibNumber" : BibNumber,
            "mail" : mail_resp
        })
    except Exception as e:
        return "Error : "+str(e)
    
def edit(body):
    try:
        ID = body["ID"]
        Details = body["DETAILS"]
        
        resp = functions.sql.basics.update(TABLE_NAME,{
            "CONDITION" : f"id = '{ID}'",
            "DATA" : Details
        },True)


        try:
            resp = int(resp)
            if(resp>1):
                return functions.sql.basics.js({
                    "status" : "fail",
                    "message" : f"There was a id mistake but, still {resp} Records Updated"
                })
            elif(resp == 0):
                return functions.sql.basics.js({
                    "status" : "fail",
                    "message" : "ID Not found"
                })
            else:#resp == 1
                return functions.sql.basics.js({
                    "status" : "success",
                    "message" : "Record Updated"
                })
        except:
            return functions.sql.basics.js({
                "status" : "fail",
                "message" : resp
            })
    except Exception as e:
        return "Error : "+str(e)
 

def get_all_forms(body):
    try:
        token = body["TOKEN"]
        searchInput = body["SEARCH_INPUT"]
        searchOn = body["SEARCH_ON"]

        resp = functions.sql.basics.getDataForToken(token)

        if(resp["status"] == "expired"):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"session timed out"
            })
        
        # Id ,EMAIL ,NAME ,AGE ,FNAME ,MNAME ,GENDER ,ADDR ,STD ,SEC ,RegisteredTime ,BibNumber 
        if(searchInput == ""):
            CONDITION = "ORDER BY bibnumber ASC"
        else:
            searchInput = searchInput.replace("'","")
            Where = ""
            if(searchOn == "*"):
                qry = ""
                for col in ["name","BibNumber","email","address","mobilenum","clubname","coachname"]:
                    if(col == "BibNumber"):
                        try:
                            qry += f"{col} = {int(searchInput)-1000} or "
                        except:
                            qry += "false or "
                    else:
                        qry += f"{col} ilike '%{searchInput}%' or "
                Where = qry[:-3]
            else:
                if(searchOn == "BibNumber"):
                    Where = f"{searchOn} = {int(searchInput)-1000}"
                else:
                    Where = f"{searchOn} ilike '%{searchInput}%'"
            # CONDITION = f"WHERE name like '%{searchInput}%' ORDER BY bibnumber ASC"
            CONDITION = f"WHERE {Where} ORDER BY bibnumber ASC"
        resp = functions.sql.basics.get(TABLE_NAME,{
            "COLUMNS":"id,name,dob,age,gender,tshirtsize,address,mobilenum,email,event,agegroup,bowcat,spotcat,clubname,coachname,RegisteredTime,BibNumber ",
            "CONDITION": CONDITION
        },True)

        return functions.sql.basics.js({
            "status" : "success",
            "data" : resp
        })

    except Exception as e:
        return "Error : "+str(e)
    

def delete_forms(body):
    try:
        token = body["TOKEN"]
        IDs = body["IDs"]
        
        resp = functions.sql.basics.getDataForToken(token)

        if(resp["status"] == "expired"):
            return functions.sql.basics.js({
                "status":"fail",
                "message":"session timed out"
            })
        
        ids = ""
        for id_ in IDs:
            ids += f"'{id_}',"
        
        if(ids != ""):
            ids = ids[:-1]


        functions.sql.basics.run(TABLE_NAME,{
            "QUERY" : f"INSERT INTO form_backup SELECT * FROM form WHERE id IN ({ids});"
        })

        resp = functions.sql.basics.delete(TABLE_NAME,{
            "COLUMNS":"*",
            "CONDITION": f"id in ({ids});"
        })

        resp = int(functions.sql.basics.reverse_js(resp))

        return functions.sql.basics.js({
            "Deleted" : resp
        })
    except Exception as e:
        return "Error : "+str(e)