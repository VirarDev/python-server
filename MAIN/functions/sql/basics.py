import functions.sql.handler
import json

getDb = functions.sql.handler.getDb
from decimal import Decimal
import time
import uuid


def get_current_epoch_time():
    # Get the current time in seconds since the epoch
    current_epoch_time = int(time.time())
    return current_epoch_time

def js(resp):
    try:
        # Convert Decimal objects to float or int before serializing
        resp_serialized = json.dumps(resp, default=lambda o: int(o) if o == int(o) else float(o) if isinstance(o, Decimal) else o)
        return resp_serialized
    except Exception as e:
        print(e)

def reverse_js(json_string):
    try:
        obj = json.loads(json_string)
        return obj
    except Exception as e:
        print(e)

def get(TABLE_NAME,body,localUse=False):
    try:
        cols = body["COLUMNS"]
        cond = body["CONDITION"]
        if(localUse):
            return functions.sql.handler.select(TABLE_NAME,cols, cond)
        else:
            return js(functions.sql.handler.select(TABLE_NAME,cols, cond))
    except Exception as e:  
        return "Error : "+str(e)
    
def count(TABLE_NAME,body,localUse=False):
    try:
        cond = body["CONDITION"]
        if(localUse):
            return functions.sql.handler.count(TABLE_NAME, cond)
        else:
            return js(functions.sql.handler.count(TABLE_NAME, cond))
    except Exception as e:
        return "Error : "+str(e)
    

def store(TABLE_NAME,body):
    try:
        id = body["ID"]
        data = body["DATA"]
        return functions.sql.handler.insert(TABLE_NAME,id, data)
    except Exception as e:
        return "Error : "+str(e)


def update(TABLE_NAME,body,localUse=False):
    try:
        data = body["DATA"]
        cond = body["CONDITION"]
        if(localUse):
            return functions.sql.handler.update(TABLE_NAME,cond, data)
        else:
            return js(functions.sql.handler.update(TABLE_NAME,cond, data))
    except Exception as e:  
        return "Error : "+str(e)
    

def delete(TABLE_NAME,body):
    try:
        cond = body["CONDITION"]
        return js(functions.sql.handler.delete(TABLE_NAME,cond))
    except Exception as e:
        return "Error : "+str(e)


def run(TABLE_NAME,body,localUse=False):
    try:
        qry = body["QUERY"]
        if(localUse):
            return functions.sql.handler.direct_query(TABLE_NAME,qry)
        else:
            return js(functions.sql.handler.direct_query(TABLE_NAME,qry))
    except Exception as e:
        return "Error : "+str(e)
    
def get_columns(TABLE_NAME,localUse=False):
    try:
        if(localUse):
            return functions.sql.handler.get_column_names(TABLE_NAME)
        else:
            return js(functions.sql.handler.get_column_names(TABLE_NAME))
    except Exception as e:
        return "Error : "+str(e)

def pragma(TABLE_NAME):
    try:
        return js(functions.sql.handler.pragma(TABLE_NAME))
    except Exception as e:
        return "Error : "+str(e)
    

def getTokenForData(Data):
    try:
        jsonData = js(Data)
        ID = str(uuid.uuid4())

        store("tokens",{
            "ID":ID,
            "DATA": {
                "Data":jsonData,
                "expiryEpoch":get_current_epoch_time()+3600 #1 hour expiry
            }
        })
        return ID
    except Exception as e:
        return "Error : "+str(e)


def getDataForToken(TokenID):
    try:
        currentEpoch = get_current_epoch_time()

        tokens = get("tokens",{
            "COLUMNS": "Data",
            "CONDITION": f"WHERE ID = '{TokenID}' AND expiryEpoch >= {currentEpoch}"
        },True)[1:]

        if(len(tokens) == 0):
            return {
                "status":"expired"
            }
        
        jsonData = tokens[0][0]
        Data = reverse_js(jsonData)

        return {
            "status":"success",
            "data":Data
        }

    except Exception as e:
        return "Error : "+str(e)