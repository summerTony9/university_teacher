import random
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

df = pd.read_csv('teacher_info-raw.csv')
print(df.head())

info_list = []
name_list = []

for index in range(len(df)):
    print(index)
    teacher_name = df.loc[index, '姓名']
    teacher_url = df.loc[index, 'url']
    html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    # print(bs0bj.contents)

    table = bs0bj.find('td', {"style": "padding:10px; "})
    info = table.get_text()
    info_list.append(info)
    name_list.append(teacher_name)
    time.sleep(np.random.uniform(1, 3))

full_df = pd.DataFrame(
    {'姓名': name_list,
     '简介': info_list}
)

df.merge(full_df, on='姓名').to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')

