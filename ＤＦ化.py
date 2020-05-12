# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import datetime
import numexpr

now = datetime.datetime.now()
dbname = "stocks.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# dbをpandasで読み出す。
df = pd.read_sql('SELECT * FROM brands', conn)

cur.close()
conn.close()

df_v1 =df[df['volume'].str.contains('百万円')]
df_r = df_v1.replace('百万円','', regex=True)
df_r2 = df_r.replace(',','', regex=True)
df_r3 = df_r2.replace('－','', regex=True)
df_r4 = df_r3['volume'].str.rstrip()
#df_s = df_r4['volume'].astype(str)
#df_i = df_s['volume'].astype(int)
df_d =df.drop(columns=['volume'])
df_a = pd.concat([df_d,df_r4],axis =1)
df_v =df_a[df.values == '東証１']
df_i = df_v.astype({'volume': int})
print(df_i)

#print(df_v['volume'].map(type))
#df_s1 = df_v.query('volume > 100')
#df_s1.to_csv(now.strftime("%Y_%m_%d")+ ".csv",encoding="utf-8-sig")
