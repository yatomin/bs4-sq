import requests
from bs4 import BeautifulSoup
import datetime
import schedule
import time

now = datetime.datetime.now()
code = 1357
load_url = 'https://www.traders.co.jp/stocks_info/individual_info_basic.asp?SC={}%20&MC=00&TYPE='.format(code)
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

MA25 = soup.find_all(class_ = 'basic_value_tech')[4]
price = soup.find_all(class_ = 'price')[0:3]
volume = soup.find_all('tr')[174].find_all('td')[3]
date = now.strftime("%Y")+'年'+str(int(now.strftime("%m")))+'月'+now.strftime("%d")+'日'

