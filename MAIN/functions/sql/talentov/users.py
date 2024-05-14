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
