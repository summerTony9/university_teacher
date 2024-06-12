from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

df = pd.read_csv('teacher_info.csv')
print(df.head())

names = []
infos = []

result_list = []
for index in range(len(df)):
    teacher_name = df.loc[index, '姓名']
    teacher_url = df.loc[index, 'url']
    if teacher_url[-4:] == '.htm':
        html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}).content
        bs0bj = BeautifulSoup(html, features='html.parser')
        teacher_info = bs0bj.find('div', {'class': 'v_news_content'}).get_text()
        names.append(teacher_name)
        infos.append(teacher_info)

result_df = pd.DataFrame(
    {'姓名': names,
     '信息': infos}
)

df.merge(result_df, on='姓名', how='left').to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')
