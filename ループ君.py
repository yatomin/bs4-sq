# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 11:13:00 2020

@author: fukam
"""
import datetime
import schedule
import time
import pandas as pd
import numpy as np
import sqlite3
import requests
import pandas.io.sql as psql

"""
    now = datetime.datetime.now()
    df = pd.read_csv(now.strftime("%Y_%m_%d")+ ".csv")
    df['5日平均比出来高急増率'] = df['5日平均比出来高急増率'].str.replace('%', '')
    df_fcol = df.astype({'5日平均比出来高急増率': float})
    df_fcol2 = df_fcol.astype({'出来高': float})
    df_fcol2['trading_value'] = df_fcol2['取引値.1']*df_fcol2['出来高'] 
    df_l = df_fcol2['コード'].values.tolist()
    print(df_l)
"""
def collect_date():
    # sqlite3に接続
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()    
    # Select文からDataFrameを作成
    df = psql.read_sql("SELECT * FROM brands", con)
    df_l = df['コード'].values.tolist()
    for brand in df_l:
        url = 'https://kabuoji3.com/stock/{}/'.format(brand)
        df = pd.read_html(url)
        """
        query = 'create table 銘柄_{} (日付 text, 始値 integer, 高値 integer, 安値 integer, 終値 integer, 出来高 integer, 終値調整 integer)'.format(brand)
        cur.execute(query)
        """
        df[0].to_sql('銘柄_{}'.format(brand),con,if_exists='replace',index=None)
        print(df[0])
        time.sleep(5)

def ATR_cal():
    #日付計算　→　使わないｗ
    now = datetime.datetime.now()
    days_20ago = now - datetime.timedelta(days=20)
    now_str = now.strftime('%Y-%m-%d')
    days_20ago_str = days_20ago.strftime('%Y-%m-%d')
    now_custom = datetime.datetime.strptime(now_str, '%Y-%m-%d')
    days_20ago_custom = datetime.datetime.strptime(days_20ago_str, '%Y-%m-%d')
    #２ATR
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()    
    df = psql.read_sql("SELECT * FROM 銘柄_2151", con)
    df['a'] = df['終値'] - df['安値']
    df['b'] = df['終値'] - df['高値']
    df['c'] = df['高値'] - df['安値']
    df['MAX'] = df[['a','b','c']].max(axis =1)
    dfe = df.iloc[1:25,[0,10]] 
    dfa = dfe.mean()
    print(dfa.tolist())
#if文、もしATRあれば記入しないにする！それと銘柄の部分は｛｝でformat文をいれる

def Average_deviation_rate():
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()    
    df = psql.read_sql("SELECT * FROM 銘柄_2151", con)
    df_choose = df.iloc[1:25,[0,4]] 
    dfa = df_choose.mean()
    print(dfa.tolist())
    
def Half_the_value():
    con = sqlite3.connect('管理君.db')
    cur = con.cursor()    
    df = psql.read_sql("SELECT * FROM 銘柄_2151", con)
    half_the_value = df.iat[1,1] -( df.iat[1,1] - df.iat[1,4])/2  
    print(half_the_value.tolist())
    
if __name__ == '__main__':
    ATR_cal()
    Average_deviation_rate()
    Half_the_value()