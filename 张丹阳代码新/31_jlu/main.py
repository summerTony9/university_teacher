import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://ciee.jlu.edu.cn/szdw.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

teachers = bs0bj.find('div', {'class': "readcontent"})
teachers = teachers.find_all('a')
names = [teacher.get_text().strip() for teacher in teachers]
urls = [teacher.get('href') for teacher in teachers]
df = pd.DataFrame(
    {'姓名': names,
     'url': urls}
)

df = df[df['url'].isnull() == False]
df['url'] = df['url'].apply(lambda x: "https://ciee.jlu.edu.cn/" + x)
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
