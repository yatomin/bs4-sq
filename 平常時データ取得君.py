# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import schedule
import time
import sqlite3

"""スクレイピング
MA25 = soup.find_all(class_ = 'basic_value_tech')[4]
start_price = soup.find_all(class_ = 'price')[0]
closing_price = soup.find_all('span')[7]
high_price = soup.find_all(class_ = 'price')[1]
low_price = soup.find_all(class_ = 'price')[2]
volume = soup.find_all('tr')[174].find_all('td')[3]
date = now.strftime("%Y")+'年'+str(int(now.strftime("%m")))+'月'+now.strftime("%d")+'日'
sector = soup.find_all(class_ = 'default_link')[1]
code = soup.find_all('span')[6]
name = soup.find_all('td')[165]
"""

now = datetime.datetime.now()
code_range = range(1301,9998)
stocks = r'C:\Users\Owner\iCloudDrive\プログラミング\爆上げ銘柄管理君\銘柄データ収集\stocks.db'

def get_brand(code):
    load_url = 'https://www.traders.co.jp/stocks_info/individual_info_basic.asp?SC={}%20&MC=00&TYPE='.format(code)
    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    if len(soup.find_all('td')[165].text()) == 0:
        return None

    try:
        code = soup.find_all('span')[6].text()
        name = soup.find_all('td')[165].text()
        sector = soup.find_all(class_ = 'default_link')[1].text
        date = now.strftime("%Y")+'年'+str(int(now.strftime("%m")))+'月'+now.strftime("%d")+'日'
        start_price = soup.find_all(class_ = 'price')[0]
        closing_price = soup.find_all('span')[7]
        high_price = soup.find_all(class_ = 'price')[1]
        low_price = soup.find_all(class_ = 'price')[2]
        MA25 = soup.find_all(class_ = 'basic_value_tech')[4]
        volume = soup.find_all('tr')[174].find_all('td')[3]
    except (ValueError, IndexError):
        return None

    return code, name, sector, date, start_price, closing_price, high_price, low_price, MA25, volume 

def brands_generator(code_range):
    for code in code_range:
        brand = get_brand(code)
        if brand:
            yield brand
    time.sleep(1)

def insert_brands_to_db(stocks,code_range):
  conn = sqlite3.connect(stocks)
  with conn:
    stocks = 'INSERT INTO stocks(code, name, sector, date, start_price, closing_price, high_price, low_price, MA25, volume) ' \
          'VALUES(?,?,?,?,?,?,?,?,?,?)'
    conn.executemany(stocks, brands_generator(code_range))

if __name__ == '__main__':
    brands_generator(code_range)
    insert_brands_to_db(stocks,code_range)    
   
