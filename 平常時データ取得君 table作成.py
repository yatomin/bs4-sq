# -*- coding: utf-8 -*-
import sqlite3
import datetime
import schedule
import time

DATABASE = 'db_file_name.db'
conn = sqlite3.connect(DATABASE)
now = datetime.datetime.now()

def create_table():
    now = datetime.datetime.now()
    now = now.strftime("%Y_%m_%d")
    f ='''CREATE TABLE IF NOT EXISTS {now}
             (code INTEGER PRIMARY KEY,
              name TEXT,
              sector TEXT,
              date INTEGER,
              start_price INTEGER,
              high_price INTEGER,
              low_price INTEGER,
              MA25 INTEGER,
              volume INTEGER)'''
    conn.execute(f)
    conn.commit()
if __name__ == '__main__':
    create_table()
   
"""
code, name, sector, date, start_price, closing_price, high_price, low_price, MA25, volume 
"""