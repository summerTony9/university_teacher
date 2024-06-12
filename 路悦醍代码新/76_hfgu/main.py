import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://yqkx.hfut.edu.cn/szdwx/list.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)

infos = bs0bj.find('div', {'class': "sz-cont"})
infos = infos.find_all('li')
pre = "https://yqkx.hfut.edu.cn"
name_list = []
url_list = []

for info in infos:
    name = info.get_text()
    name = re.sub('[^\u4e00-\u9fa5]+', '', name)
    url = info.find('a').get('href')
    url = pre + url
    name_list.append(name)
    url_list.append(url)

full_df = pd.DataFrame(
    {'姓名': name_list,
     'url': url_list}
)

full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')