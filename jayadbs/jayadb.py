import sqlite3

import os
Db = "GC.db"
TABLE_NAME = "GC"

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(Db)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()


q = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} "+qry+";"
cursor.execute(q)



cursor.close()
conn.commit()
conn.close()
