import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://zhijian.hbu.edu.cn/info_show.asp?infoid=174"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)

table = bs0bj.find('td', {'width': '911'})
infos = table.find_all('a')
pre = "https:"

names = []
urls = []
for info in infos:
    name = info.get_text().replace("\n", "")
    name = re.sub('[^\u4e00-\u9fa5]+', '', name)
    href = info.get('href')
    if href is None:
        url = ''
    else:
        url = pre + href
    names.append(name)
    urls.append(url)

full_df = pd.DataFrame(
    {'姓名': names,
     'url': urls}
)

full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')