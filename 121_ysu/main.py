from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://iee.ysu.edu.cn/iee6/teacher/teacher2.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

table = bs0bj.find('table', attrs={'id': 'aaa'})
table_df = pd.read_html(str(table))[0]
table_df = table_df[['姓名', '性别', '职称', '导师级别']]

all_info = table.find_all('a', attrs={'class': 'tit'})

teacher_names = [info.get('title') for info in all_info]
teacher_urls = [info.get('href') for info in all_info]

url_df = pd.DataFrame(
    {'姓名': teacher_names,
     'url': teacher_urls}
)

full_df = table_df.merge(url_df, how='left', on=['姓名'])
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
