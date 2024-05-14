# import sqlite3

import psycopg2
# Define your PostgreSQL connection string
# DATABASE_URL = "postgresql://AllData_owner:o8FXzqEfLvB9@ep-divine-bird-a1cvtabe-pooler.ap-southeast-1.aws.neon.tech/AllData?sslmode=require"
# DATABASE_URL = "postgresql://jay:1234@15.207.19.99:5432/talentov"
# DATABASE_URL = "postgresql://jay:1234@0.0.0.0:5432/talentov"

DATABASE_URL_Talentov = "postgresql://jay:1234@15.207.19.99:5432/talentov"
# DATABASE_URL_Talentov = "postgresql://jay:1234@0.0.0.0:5432/talentov"

DATABASE_URL_Virar = "postgresql://jay:1234@15.207.19.99:5432/virardb"
# DATABASE_URL_Virar = "postgresql://jay:1234@0.0.0.0:5432/virardb"

DATABASE_URL_Vellore = "postgresql://jay:1234@15.207.19.99:5432/vellore"
# DATABASE_URL_Vellore = "postgresql://jay:1234@0.0.0.0:5432/vellore"


import sys

connection_pool = ""

# Create a connection
if(sys.PORT_NUMBER == 5000):
    connection_pool = psycopg2.connect(DATABASE_URL_Talentov)
elif(sys.PORT_NUMBER == 50087):
    connection_pool = psycopg2.connect(DATABASE_URL_Virar)
elif(sys.PORT_NUMBER == 50088):
    connection_pool = psycopg2.connect(DATABASE_URL_Vellore)
else:
    pass

print(sys.PORT_NUMBER,connection_pool)


class SQLite:
    def __init__(self,path):
        # self.conn = sqlite3.connect(path)
        self.conn = connection_pool
        self.cur = self.conn.cursor()
    def cur(self):
        return self.cur
    def exe(self,qry):
        try:
            self.cur.execute(qry)
            return "ok"
        except Exception as e:
            return "Error : "+str(e)
    def close(self):
        try:
            self.conn.commit()
        except:
            pass
        # self.conn.close()
        self.cur.close()

connection = ""

def getDb(TABLE_NAME):
    return SQLite(TABLE_NAME)
    # return SQLite("db/"+TABLE_NAME+".db")

def getTable(TABLE_NAME):
    if("/" in TABLE_NAME):
        return TABLE_NAME.split("/")[-1]
    else:
        return TABLE_NAME
    
def insert(TABLE_NAME,id,data):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    values = tuple()
    cols = ""
    inp = ""

    for key,val in data.items():
        inp += ",%s"
        values += (val,)
        cols += f",{key}"
        
    try:
        db.cur.execute(f"INSERT INTO {TABLE_NAME} (id{cols}) VALUES (%s{inp})", (id,)+values)
        db.close()
        return "ok"
    except Exception as e:
        db.close()
        return "Error : "+str(e)


def update(TABLE_NAME,condition,data):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    values = tuple()
    upd = ""

    row = 0
    for key,val in data.items():
        if row > 0:
            upd+= ","
        upd += f"{key}=%s"
        values += (val,)
        row += 1
        
    try:
        # print(f"UPDATE {TABLE_NAME} SET {upd} WHERE {condition}")
        db.cur.execute(f"UPDATE {TABLE_NAME} SET {upd} WHERE {condition}", values)
        num_updated = db.cur.rowcount
        db.close()
        return str(num_updated)
    except Exception as e:
        db.close()
        return "Error : "+str(e)


def select(TABLE_NAME, cols, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"SELECT {cols} FROM {TABLE_NAME} {cond}")
    if res == "ok":
        comps = db.cur.fetchall()
        resp = []
        column_names = [desc[0] for desc in db.cur.description]
        resp = [column_names] + comps
        db.close()
        return resp
    else:
        db.close()
        return res

def count(TABLE_NAME, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"SELECT COUNT(ID) FROM {TABLE_NAME} {cond}")
    if res == "ok":
        count = db.cur.fetchone()[0]
        db.close()
        return count
    else:
        db.close()
        return res


def delete(TABLE_NAME, cond=""):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"DELETE FROM {TABLE_NAME} WHERE {cond}")
    if res == "ok":
        num_deleted = db.cur.rowcount
        db.close()
        return str(num_deleted)
    else:
        db.close()
        return res


def direct_query(DB_PATH, query=""):
    # if query.strip().lower().startswith("create table"):
    #     # For CREATE TABLE queries
    #     return "Restricted Query"
    # elif query.strip().lower().startswith("drop table"):
    #     # For CREATE TABLE queries
    #     return "Restricted Query"

    db = getDb(DB_PATH)
    res = db.exe(query)
    if res == "ok":
        if query.strip().lower().startswith("select"):
            comps = db.cur.fetchall()
            db.close()
            return comps
        elif query.strip().lower().startswith(("insert", "update", "delete")):
            # For INSERT, UPDATE, DELETE queries
            affected_rows = db.cur.rowcount
            db.close()
            return affected_rows
        else:
            # For other queries (e.g., ALTER TABLE, DROP TABLE, etc.)
            db.close()
            return "Query executed successfully"
    else:
        db.close()
        return res


def get_column_names(TABLE_NAME):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    # res = db.exe(f"PRAGMA table_info({TABLE_NAME})")
    q = f"SELECT data_type,column_name FROM information_schema.columns WHERE table_name = '{TABLE_NAME.lower()}';"
    res = db.exe(q)
    if res == "ok":
        columns = [row[1] for row in db.cur.fetchall()]
        db.close()
        return columns
    else:
        db.close()
        return res


def pragma(TABLE_NAME):
    db = getDb(TABLE_NAME)
    TABLE_NAME = getTable(TABLE_NAME)
    res = db.exe(f"PRAGMA table_info({TABLE_NAME})")
    if res == "ok":
        columns = db.cur.fetchall()
        db.close()
        return columns
    else:
        db.close()
        return res


    