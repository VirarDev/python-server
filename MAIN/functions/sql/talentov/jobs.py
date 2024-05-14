import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

TABLE_NAME = get_table_name()

import functions.sql.basics as base

get = lambda body:base.get(TABLE_NAME,body)
count = lambda body:base.count(TABLE_NAME,body)
store = lambda body:base.store(TABLE_NAME,body)
update = lambda body:base.update(TABLE_NAME,body)
delete = lambda body:base.delete(TABLE_NAME,body)
run = lambda body:base.run(TABLE_NAME,body)
def get_columns():return base.get_columns(TABLE_NAME)
def pragma():return base.pragma(TABLE_NAME)


def job_init_data(body):
    try:
        JOBID = body["JOBID"]

        JOB_DETAIL = base.get(TABLE_NAME,{
            "COLUMNS": "id,Name,Comid,Description,Opening,Closed,Status,UserList,Comment,Spocid,CreatedBy,CreatedOn,CreatedOnMS",
            "CONDITION": f"WHERE id = '{JOBID}'"
        },True)[1]

        COMID = JOB_DETAIL[2]

        COMP_NAME = base.get("COMPANY",{
            "COLUMNS": "Name",
            "CONDITION":f"WHERE id='{COMID}'"
        },True)[1][0]

        spocs = base.get("SPOC",{
            "COLUMNS": "id,NAME,Mail,Comid",
            "CONDITION":f"WHERE Comid='{COMID}'"
        },True)[1:]

        AllUsers = base.get("USERS",{
            "COLUMNS": "id,Name",
            "CONDITION": ""
        },True)[1:]

        return base.js({
            "JOB_DETAIL": JOB_DETAIL,
            "COMID": COMID,
            "COMP_NAME": COMP_NAME,
            "spocs": spocs,
            "AllUsers": AllUsers
        })
    except Exception as e:
        return "Error : "+str(e)


def jobs_init_data(body):
    try:
        COMID = body["COMID"]

        company = base.get("COMPANY",{
            "COLUMNS": "Name",
            "CONDITION": f"WHERE id = '{COMID}'"
        },True)[1][0]

        AllUsers = base.get("USERS",{
            "COLUMNS": "id,Name",
            "CONDITION": ""
        },True)[1:]
        
        AllUserNamesObj = {}
        for user in AllUsers:
            AllUserNamesObj[user[0]] = user[1]

        spocs = base.get("SPOC",{
            "COLUMNS": "id,NAME,Mail,Comid",
            "CONDITION":f"WHERE Comid='{COMID}'"
        },True)[1:]

        
        # listJobs = base.get("JOBS",{
        #     "COLUMNS": "id,Description,Name,Opening,Comid,Closed,Status,UserList,Comment,Spocid,CreatedBy,CreatedOn,CreatedOnMS",
        #     "CONDITION": "WHERE Comid='"+COMID+"'",
        # },True)

        return base.js({
            "company": company,
            "COMID": COMID,
            "spocs": spocs,
            "AllUserNamesObj": AllUserNamesObj,
            # "listJobs":listJobs
        })
    except Exception as e:
        return "Error : "+str(e)

