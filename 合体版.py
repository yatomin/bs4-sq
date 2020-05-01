import pandas as pd
import datetime
import time
from openpyxl import Workbook,load_workbook
from pprint import pprint
import os, tkinter, tkinter.filedialog, tkinter.messagebox
from os import path
import csv
import sqlite3
import datetime


now = datetime.datetime.now()
df = pd.read_csv(now.strftime("%Y_%m_%d")+ ".csv",usecols=[2,3,5,6,7,8,9,10,11,12])
#df = pd.read_csv("2020_04_15.csv",usecols=[2,3,5,6,7,8,9,10,11,12])
df = (df[df['出来高'] > 1000000])
df = df.reset_index()
#df.to_csv("2020_04_15加工済み.csv",encoding="utf-8-sig")
df.to_csv(now.strftime("%Y_%m_%d")+ "加工済み.csv",encoding="utf-8-sig")

db_file='管理君.db'
con = sqlite3.connect(db_file)
now = datetime.datetime.now()

cursor = con.cursor()
cursor.execute(" CREATE TABLE IF NOT EXISTS 管理君 ('index','id', 'コード', '名称',  '取引値', '取引値_1', '前日比', '前日比_1', '第5日平均比出来高急増率', '出来高', '高値', '安値')")
def get_filename(filetype):
# ファイル選択ダイアログ
    print(filetype+'ファイルを選択してください')
    root = tkinter.Tk()
    root.attributes("-topmost", True)#最前面化、他の画面の裏に埋もれて強制終了しまくったヽ(`Д´)ﾉ ﾌﾟﾝﾌﾟﾝ
    root.withdraw()
    fTyp = [("","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    return file

csv_filename=get_filename(now.strftime("%Y_%m_%d")+ "加工済み.csv")
with open(csv_filename,'r',encoding="utf-8_sig",newline='') as fp: # `with` statement available in 2.5+
    rows=csv.reader(fp)
    for row in rows:
        print(row)
        cursor.execute("INSERT INTO 管理君 VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",row)
    con.commit()
con.close
