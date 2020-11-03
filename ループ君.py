# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:13:00 2020

@author: fukam
"""
import schedule
import time
import pandas as pd
import numpy as np
import sqlite3
import requests
import pandas.io.sql as psql
from datetime import datetime
import datetime
import os

def collect_date_neo():
    # sqlite3に接続
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()    
    # Select文からDataFrameを作成
    df = psql.read_sql("SELECT * FROM brand", con)
    df_l = df['コード'].values.tolist()
    for brand in df_l:
        stocks = r'C:\Users\Owner\iCloudDrive\プログラミング\爆上げ銘柄管理君\csv\csv格納\銘柄時系列\{}.csv'.format(brand)
        df = pd.read_csv(stocks, encoding="cp932")
        df2 = pd.to_datetime(df['日付'], format='%Y%m%d')
        df3 = df.drop('日付',axis=1)
        df4 = pd.concat([df3,df2],axis=1)        
        df4.to_sql('銘柄_{}'.format(brand),con,if_exists='replace',index=None)
        os.remove(r'C:\Users\Owner\iCloudDrive\プログラミング\爆上げ銘柄管理君\csv\csv格納\銘柄時系列\{}.csv'.format(brand))
        print(df)
        time.sleep(1)

def sum_count():
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d')
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()   
    df_brands = psql.read_sql("SELECT * FROM brand", con)
    df_l = df_brands['コード'].values.tolist()
    df_n = df_brands['名称'].values.tolist()
    AVG = []
    for code in df_l:
        df = psql.read_sql("SELECT * FROM 銘柄_{}".format(code), con)
        df_25 = df.iloc[0,3]>df.iloc[0,5]
        AVG.append(df_25)   
    df_AVG = pd.DataFrame(AVG,columns=['avg'])
    df_merge1 = pd.concat([df_brands,df_AVG],axis=1)
    print(df_merge1)
    df_merge2 = df_merge1[df_merge1.avg]
    print(df_merge2)
    df_merge3 = df_merge2.drop('avg', axis=1)
    print(df_merge3)
    file_sqlite3 = "管理君.db"
    conn = sqlite3.connect(file_sqlite3)
    df_merge2.to_sql('brands_neo',conn,if_exists='replace',index=None)
    df_merge3.to_sql('brand',conn,if_exists='replace',index=None)
    conn.close()
    
def type():
    #datatype検索
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()   
    df_brands = psql.read_sql("SELECT * FROM brand", con)
    df_l = df_brands['コード'].values.tolist()
    df_n = df_brands['名称'].values.tolist()
    for code in df_l:
        df = psql.read_sql("SELECT * FROM 銘柄_{}".format(code), con)
        df['日付'] = pd.to_datetime(df['日付'])
        print(df.dtypes)
    
def most_recent_high():
    #日付の範囲指定　datetime型に変換　→　範囲指定をすること
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()   
    df= psql.read_sql("SELECT * FROM 銘柄_2151", con)
    df['日付'] = pd.to_datetime(df['日付'], format='%Y-%m-%d')
    dfa = df[df['日付'] > pd.Timestamp.today()]
    print(dfa)
    df= psql.read_sql("SELECT * FROM 銘柄_2151", con)

def join_columns():
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()   
    df_brands = psql.read_sql("SELECT * FROM brand", con)
    df_c = df_brands['コード'].values.tolist()
    df_n = df_brands['名称'].values.tolist()
    finish =[]
    for code in df_c:
        df = psql.read_sql("SELECT * FROM 銘柄_{}".format(code), con)
        df_f= df.iloc[0,4]
        finish.append(int(df_f))
        #25日と直近をいれること
    df1 = pd.DataFrame({'コード': df_c,
                    '名称': df_n,
                    '終値': finish})
    print(df1)    

if __name__ == '__main__':
    collect_date_neo()
    sum_count()
    #今日
    #now = dt.date.today()
    #print(now)