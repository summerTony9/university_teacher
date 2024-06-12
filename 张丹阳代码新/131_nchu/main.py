import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

url = 'http://dscx.yjs.nchu.edu.cn/college.html?collegeId=8&page=1'
info_list = []

for i in range(13):
    url = 'http://dscx.yjs.nchu.edu.cn/college.html?collegeId=8&page=' + str(i)
    html = requests.get(url, headers={'User-agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, 'html.parser')

    infos = bs0bj.find_all('div', class_ = 'xy2-list clear')
    for info in infos:
        name = info.find('p', class_='xy2-name').get_text()
        url = info.find('a')['href']
        info_list.append(
            {
                '姓名': name,
                'url': url
            }
        )


df = pd.DataFrame(info_list)
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')