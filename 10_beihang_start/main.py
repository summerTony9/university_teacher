import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


def get_infos(url):
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    infos = bs0bj.find('div', {'class': "ldtz"}).find_all('li')
    names = [info.find('h3').get_text().strip() for info in infos]
    urls = []
    for info in infos:
        url_temp = info.find('a').get('href')
        url_temp = re.search(r"info.*", url_temp).group()
        urls.append("https://yqgdxy.buaa.edu.cn/" + url_temp)
    return pd.DataFrame(
        {'姓名': names,
         'url': urls}
    )


depts = pd.read_csv('dept.csv')
df_list = []

for index in range(len(depts)):
    print(depts.loc[index, 'url'])
    url = depts.loc[index, 'url']
    dept = depts.loc[index, '研究室']
    for i in range(depts.loc[index, 'pages']):
        if i == 0:
            url_new = url
        else:
            url_new = url[:-4] + '/' + str(i) + '.htm'
        df = get_infos(url_new)
        df['研究室'] = dept
        df_list.append(df)

full_df = pd.concat(df_list)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
