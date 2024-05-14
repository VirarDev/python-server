import os

def get_table_name():
    current_file = os.path.basename(__file__)
    return current_file.upper().replace(".PY","")

import json
def js(resp):
    return json.dumps(resp)


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



def get_job_states_and_spocs_for_all():
    counts = {}
    companies = base.get(TABLE_NAME,{
        "COLUMNS": "id",
        "CONDITION": ""
    },True)[1:]


    for company in companies:
        comid = company[0]

        active = base.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '0'"
        },True)
        closed = base.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '1'"
        },True)
        hold = base.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status = '2'"
        },True)
        unset = base.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}' and Status is NULL"
        },True)
        total = base.count("JOBS",{
            "CONDITION":f"WHERE Comid='{comid}'"
        },True)

        spocs = base.get("SPOC",{
            "COLUMNS": "Name",
            "CONDITION": f"WHERE Comid = '{comid}'"
        },True)[1:]

        #0 index - id
        counts[comid] = {
            "active":active,
            "closed":closed,
            "hold":hold,
            "unset":unset,
            "total":total,
            "spocs":spocs,
        }
    return js(counts)
    
