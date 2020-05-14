# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import datetime
import numpy as np
import numexpr

now = datetime.datetime.now()
dbname = "stocks.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# dbをpandasで読み出す。
df = pd.read_sql('SELECT * FROM brands', conn)

cur.close()
conn.close()

df_ex =df[df['volume'].str.contains('百万円')]
df_re1 = df_ex.replace('百万円','', regex=True)
df_re2 = df_re1.replace(',','', regex=True)
df_re3 = df_re2.replace('－','', regex=True)
df_re4 = df_re3.replace(u'\xa0', u' ', regex=True)
df_re5 = df_re4.replace("''",'1', regex=True)
df_re6 = df_re5['volume'].str.rstrip()
df_dr =df.drop(columns=['volume'])
df_a = pd.concat([df_dr,df_re6],axis =1)
df_v =df_a[df.values == '東証１']
df2 = df_v.dropna(how='all')
df3 =df2.sort_values('volume')
print(df3['volume'] == 100)
#df3.to_csv(now.strftime("%Y_%m_%d")+ ".csv",encoding="utf-8-sig")
"""
print(type(df))
df_i = df_v.astype({'volume': int})
print(df_i)
print(df_v['volume'].map(type))
df_s1 = df_v.query('volume > 100')
print(df2.isnull())
df_s = df_r4['volume'].astype(str)
df_i = df_s['volume'].astype(int)
"""
