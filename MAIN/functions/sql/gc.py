import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = "ALLUSERS"

import functions.sql.basics

get = lambda body:functions.sql.basics.get(TABLE_NAME,body)
count = lambda body:functions.sql.basics.count(TABLE_NAME,body)
store = lambda body:functions.sql.basics.store(TABLE_NAME,body)
update = lambda body:functions.sql.basics.update(TABLE_NAME,body)
delete = lambda body:functions.sql.basics.delete(TABLE_NAME,body)
run = functions.sql.basics.run
js = functions.sql.basics.js


getDb = functions.sql.basics.getDb



def get_columns():return functions.sql.basics.get_columns(TABLE_NAME)
def pragma():return functions.sql.basics.pragma(TABLE_NAME)

def mkdir(dirname):
    try:
        if(not os.path.isdir(dirname)):
            os.mkdir(dirname)
    except:
        pass
mkdir("db")

ALLUSERS_QRY = "CREATE TABLE IF NOT EXISTS "+TABLE_NAME+" (id VARCHAR(255) PRIMARY KEY,Email VARCHAR(255),Phone VARCHAR(255),FirstName VARCHAR(255),LastName VARCHAR(255),Photo VARCHAR(255),FullName VARCHAR(255));"
run(TABLE_NAME,{"QUERY":ALLUSERS_QRY},True)

USER_CHAT_LIST_TABLE_NAME = "USER_CHAT_LIST"
CHAT_LIST_TABLE_NAME = "CHAT_LIST"
CHAT_DB = "CHAT_DBS"

class Tab:
    def __init__(self,user_id):
        self.USER_ID = user_id
        self.user_chat_list = CHAT_DB+"/"+self.USER_ID+"/"+USER_CHAT_LIST_TABLE_NAME
        self.chat_list = CHAT_DB+"/"+self.USER_ID+"/"+CHAT_LIST_TABLE_NAME

def init_user(user_id):
    # USER_CHAT_LIST_TABLE_NAME = user_id + "_USER_CHAT_LIST"
    # CHAT_LIST_TABLE_NAME = user_id + "_CHAT_LIST"
    user = Tab(user_id)

    USER_CHAT_LIST_QRY = "CREATE TABLE IF NOT EXISTS "+USER_CHAT_LIST_TABLE_NAME+" (id VARCHAR(255) PRIMARY KEY,UNREAD NUMERIC,LASTMESSAGE VARCHAR(255),LASTMESSAGEMS NUMERIC);"
    # CHAT_LIST_QRY = "CREATE TABLE IF NOT EXISTS "+CHAT_LIST_TABLE_NAME+" (mid VARCHAR(255) PRIMARY KEY, id VARCHAR(255),type VARCHAR(255),isStorable BOOLEAN,isLarge BOOLEAN,previewText TEXT,content TEXT,from_user VARCHAR(255),to_user VARCHAR(255),stage INTEGER,startOn INTEGER,sentOn INTEGER,receivedOn INTEGER,viewedOn INTEGER)"
    
    # USER_CHAT_LIST_QRY = "DROP TABLE IF EXISTS "+USER_CHAT_LIST_TABLE_NAME+"";

    mkdir("db")
    mkdir("db/Conversations")
    mkdir("db/"+CHAT_DB)
    mkdir("db/"+CHAT_DB+"/"+user_id)

    run(user.user_chat_list,{"QUERY":USER_CHAT_LIST_QRY},True)
    # run(user.chat_list,{"QUERY":CHAT_LIST_QRY},True)

    return user


def get_chat_list(body):
    try:
        user_id = body["UID"]
        user = init_user(user_id)

        ids = [user_id,body["ID"]]
        ids.sort()
        conversation_id =  ids[0]+"_"+ids[1]

        count = functions.sql.basics.count("Conversations/"+conversation_id,{
            "CONDITION":""
        },True)

        count -= 10

        count = max(count,0)

        List_of_chat_messages = functions.sql.basics.get("Conversations/"+conversation_id,{"COLUMNS":"id, mid, type, isStorable, isLarge, previewText, content, from_user, to_user, stage, startOn, sentOn, receivedOn, viewedOn","CONDITION":"ORDER BY startOn ASC LIMIT 10 OFFSET "+str(count)},True)
        return js(List_of_chat_messages)
    except Exception as e:
        return "Error : "+str(e)


def add_chat_list(body):
    try:
        user_id = body["UID"]

        txt_msg = body["DATA"]["isLarge"]
        if(txt_msg == True):
            txt_msg = body["DATA"]["previewText"]
        else:
            txt_msg = body["DATA"]["content"]
        
        user_from = init_user(user_id)
        user_to = init_user(body["DATA"]["to_user"])

        
        run(user_from.user_chat_list,{"QUERY":"UPDATE "+USER_CHAT_LIST_TABLE_NAME+" SET UNREAD=0,LASTMESSAGE='"+txt_msg+"',LASTMESSAGEMS="+str(body["DATA"]["startOn"])+" WHERE id='"+body["DATA"]["to_user"]+"'"},True)
        count = run(user_to.user_chat_list,{"QUERY":"UPDATE "+USER_CHAT_LIST_TABLE_NAME+" SET UNREAD=UNREAD+1,LASTMESSAGE='"+txt_msg+"',LASTMESSAGEMS="+str(body["DATA"]["startOn"])+" WHERE id='"+user_id+"'"},True)
        if(count == 0):
            add_user_chat_list({
                "UID":body["DATA"]["to_user"],
                "ID":user_id,
                "DATA":{
                    "UNREAD":1,
                    "LASTMESSAGE":txt_msg,
                    "LASTMESSAGEMS":body["DATA"]["startOn"]
                }
            })
        

        ids = [user_id,body["DATA"]["to_user"]]
        ids.sort()
        conversation_id =  ids[0]+"_"+ids[1]
        
        if(not os.path.isfile("db/Conversations/"+conversation_id)):
            CHAT_LIST_QRY = "CREATE TABLE IF NOT EXISTS "+conversation_id+" (mid VARCHAR(255) PRIMARY KEY, id VARCHAR(255),type VARCHAR(255),isStorable BOOLEAN,isLarge BOOLEAN,previewText TEXT,content TEXT,from_user VARCHAR(255),to_user VARCHAR(255),stage NUMERIC,startOn NUMERIC,sentOn NUMERIC,receivedOn NUMERIC,viewedOn NUMERIC)"
            # CHAT_LIST_QRY = "DROP TABLE IF EXISTS "+conversation_id
            run("Conversations/"+conversation_id,{"QUERY":CHAT_LIST_QRY},True)

        return js(functions.sql.basics.store("Conversations/"+conversation_id,body))
    except Exception as e:
        return "Error : "+str(e)
    
def get_user_chat_list(body):
    try:
        user_id = body["UID"]
        user = init_user(user_id)

        List_of_chat_users = functions.sql.basics.get(user.user_chat_list,{"COLUMNS":"UNREAD,LASTMESSAGE,LASTMESSAGEMS,id","CONDITION":""},True)

        columns = List_of_chat_users[0]+functions.sql.basics.get_columns(TABLE_NAME,True)[1:]

        List_of_chat_users[0] = columns

        for i in range(1,len(List_of_chat_users)):
            try:
                other_user_record = functions.sql.basics.get(TABLE_NAME,{
                    "COLUMNS":"Email,Phone,FirstName,LastName,Photo,FullName",
                    "CONDITION":"WHERE id = '" + List_of_chat_users[i][3] + "'"
                },True)
                List_of_chat_users[i] += tuple(other_user_record[1])
            except:
                List_of_chat_users[i] += (None,)*5
        # print(List_of_chat_users)
        return js(List_of_chat_users)
    except Exception as e:
        return "Error : "+str(e)

def add_user_chat_list(body):
    try:
        user_id = body["UID"]
        user = init_user(user_id)
        return js(functions.sql.basics.store(user.user_chat_list,body))
    except Exception as e:
        return "Error : "+str(e)


def update_user_chat_list(body):
    try:
        user_id = body["UID"]
        user = init_user(user_id)
        return js(functions.sql.basics.update(user.user_chat_list,body,True))
    except Exception as e:
        return "Error : "+str(e)

def on_user_logged_in(body):
    try:
        user_count = functions.sql.basics.count(TABLE_NAME,{
            "CONDITION":"WHERE id = '" + body["ID"] + "'"
        },True)
        if(user_count == 0):
            suc = functions.sql.basics.store(TABLE_NAME,body)
            if("ok" == suc):
                return "OK"
            else:
                return suc
        else:
            suc = functions.sql.basics.update(TABLE_NAME,{
                "CONDITION":"id = '" + body["ID"]+"'",
                "DATA": body["DATA"]
            },True)
            if(suc == "1"):
                return "OK"
            else:
                return suc
    except Exception as e:
        return "Error : "+str(e)
    


