import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


url = 'https://www.tju.edu.cn/rcpy/szdw/gjyq.htm'
html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, 'html.parser')

names = bs0bj.find('tbody').find_all('p')
names = [name.get_text().strip() for name in names if name.get_text() != '']
print(names)
dict_name = {
    '姓名': names
}

df = pd.DataFrame(dict_name)
df.to_csv('优青.csv', index=False, encoding='utf-8-sig')