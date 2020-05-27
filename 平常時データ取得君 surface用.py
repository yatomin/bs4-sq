# -*- coding: utf-8 -*-
import datetime
from pyquery import PyQuery
import time
import sqlite3
import requests
import re
"""スクレイピング
MA25 = soup.find_all("span")[24]
start_price =soup.find_all("td")[23]
closing_price = soup.find_all("td")[32]
high_price = soup.find_all("td")[26]
low_price = soup.find_all("td")[29]
volume = soup.find_all("td")[36]
date = now.strftime("%Y")+'年'+str(int(now.strftime("%m")))+'月'+now.strftime("%d")+'日'
sector = soup.find_all("a")[30]
code = soup.find_all("span")[11]
name = soup.find_all("h3")[0]
"""

today = datetime.date.today()
code_range = range(1301,9998)
stocks = r'C:\Users\fukam\iCloudDrive\プログラミング\爆上げ銘柄管理君\銘柄データ収集\stocks_neo.db'
brands = range(1301,9998)
def get_brand(code):
    url = 'https://kabutan.jp/stock/?code={}'.format(code)
    url2 = 'https://kabutan.jp/stock/kabuka?code={}'.format(code)
    q = PyQuery(url)
    q2 = PyQuery(url2)
    
    if len(q.find('div.company_block')) == 0:
        return None

    try:
        MA25 = q.find('#kobetsu_right > div.kabuka_trend.clearfix > table > tbody > tr:nth-child(3) > td:nth-child(2) > span').text()
        start_price1 =q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)').text()
        closing_price1 = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(4) > td:nth-child(2)').text()
        high_price1 = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)').text()
        low_price1 = q.find('#kobetsu_left > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2)').text()
        trading_value1 = q.find('#kobetsu_left > table:nth-child(4) > tbody > tr:nth-child(2) > td').text()
        date = today
        sector = q.find('#stockinfo_i2 > div > a').text()
        market = q.find('span.market').text()
        name = q.find('#kobetsu_right > div.company_block > h3').text()
        time.sleep(1)
        volume1 = q.find('#kobetsu_left > table:nth-child(4) > tbody > tr:nth-child(1) > td').text()
        before_ratio1 = q2.find('#stock_kabuka_table > table.stock_kabuka0 > tbody > tr > td:nth-child(7) > span').text()
        start_price = int(re.sub("\\D", "", start_price1))
        closing_price = int(re.sub("\\D", "", closing_price1))
        high_price = int(re.sub("\\D", "", high_price1))
        low_price = int(re.sub("\\D", "", low_price1))
        volume = int(re.sub("\\D", "", volume1))
        trading_value= int(re.sub("\\D", "", trading_value1))
        before_ratio=  int(re.sub("\\D", "", before_ratio1))
        
    except (ValueError, IndexError):
        return None

    return code, name, market, sector, date, start_price, closing_price, high_price, low_price, MA25, volume, trading_value, before_ratio

def brands_generator(code_range):
    for code in code_range:
        brand = get_brand(code)
        if brand:
            yield brand
    time.sleep(1)

def insert_brands_to_db(stocks,code_range):
  conn = sqlite3.connect(stocks)
  with conn:
    sql = 'INSERT INTO brands(code, name, market, sector, date, start_price, closing_price, high_price, low_price, MA25, volume, trading_value, before_ratio) ' \
          'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
    conn.executemany(sql, brands_generator(code_range))

def line_send():
    url = 'https://notify-api.line.me/api/notify'
    token = 'Hm99vLGcndE2TmAoWOQwz1W118f0tHoXboiILzKF4i1'
    headers = {'Authorization' : 'Bearer ' + token}
    message =  '{} 本日の記録は完了しました。'.format(today)
    payload = {'message' : message}
    r = requests.post(url, headers=headers, params=payload)  

if __name__ == '__main__':
    brands_generator(code_range)
    insert_brands_to_db(stocks,code_range)
    line_send()
    