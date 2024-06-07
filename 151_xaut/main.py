import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

url = 'https://jyxy.xaut.edu.cn/zsjy/yjszs/ssyjszs.htm'
html = requests.get(url, {'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, 'html.parser')
infos = bs0bj.find('div', id = 'vsb_content').find_all('a')

dict_list = {
    '姓名': [],
    'url': []
}

for info in infos:
    name = info.get_text()
    url = info.get('href')
    if 'info' in url:
        url = 'https://jyxy.xaut.edu.cn/' + re.search(r"info.*", url).group()
        print(name, url)
        dict_list['姓名'].append(name)
        dict_list['url'].append(url)

df = pd.DataFrame(dict_list)
df.drop_duplicates()
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')