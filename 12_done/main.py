from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

home_url = "https://ise.hit.edu.cn/16180/list.htm"
# headers谁在访问，random随机模拟
# cookie 账号密码，本网址不需要写
# content 获取内容
html = requests.get(home_url, headers={'User-Agent': UserAgent().random}).content

# 解析字符串，不用改
bs0bj = BeautifulSoup(html, features='html.parser')

all_name = bs0bj.find("div", {"frag": "窗口6"}).find_all('ul', {'class': 'wp_subcolumn_list'})

df_list = []
for dept_info in all_name:
    dept_name = dept_info.find('h3', {'class': 'sublist_title'}).get_text()
    teacher_urls = dept_info.find_all('div', {'class': 'news_title'})
    urls = [teacher_url.find('a').get('href') for teacher_url in teacher_urls]
    names = [teacher_url.find('a').get_text() for teacher_url in teacher_urls]
    dept_names = [dept_name for _ in range(len(names))]
    df_list.append(pd.DataFrame({'dept_name': dept_names, 'name': names, 'url': urls}))

df = pd.concat(df_list)
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
