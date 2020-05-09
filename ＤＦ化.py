# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

dbname = "stocks.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# dbをpandasで読み出す。
df = pd.read_sql('SELECT * FROM brands', conn)

print(df)

cur.close()
conn.close()
