import sqlite3
import datetime
import schedule
import time

DATABASE = 'db_file_name.db'
conn = sqlite3.connect(DATABASE)
now = datetime.datetime.now()

def create_table():
    sql = '''CREATE TABLE IF NOT EXISTS now.strftime("%Y_%m_%d")
             (id INTEGER PRIMARY KEY,
              app_url TEXT,
              app_name TEXT,
              store_url TEXT)'''
    conn.execute(sql)
    conn.commit()