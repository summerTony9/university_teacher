import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


base_url = "https://mse.hust.edu.cn/szdw/jsml/jsml/qb.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

js_menu = bs0bj.find('div', {'class': 'js_menu'})
js_menu = js_menu.find_all('a', {'target': '_blank'})
urls = ["https://mse.hust.edu.cn/" + item['href'][9:] for item in js_menu]
names = [item.get_text() for item in js_menu]

df = pd.DataFrame(
    {'姓名': names,
     'url': urls}
)

df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')