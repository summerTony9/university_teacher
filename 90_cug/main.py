import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

url = "https://au.cug.edu.cn/szdw/jsml.htm"
html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.prettify())


data = []

sections = bs0bj.find_all('div', class_='teacher_lb')

for section in sections:
    current_title = None
    for element in section.children:
        if element.name == 'h4':
            department = element.get_text(strip=True)
        elif element.name == 'h6':
            current_title = element.get_text(strip=True)
        elif element.name == 'ul' and current_title:
            for li in element.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    name = a_tag.get_text(strip=True)
                    link = a_tag['href']
                    data.append([department, current_title, name, link])

# Create DataFrame
df = pd.DataFrame(data, columns=['系', '职称', '姓名', '链接'])
print(df)
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')