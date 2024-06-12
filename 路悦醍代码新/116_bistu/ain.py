import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

with open('北京信息科技大学-仪器科学与光电工程学院.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# 定义一个列表来存储老师的院系和链接
data = []

# 找到所有院系部分
departments = soup.find_all('div', class_='zhy_list')

for department in departments:
    # 获取院系名称
    department_name_tag = department.find('p', class_='zhy_lmmc')
    if department_name_tag:
        department_name = department_name_tag.text.strip()
    else:
        print("Warning: Could not find department name in one of the divs.")
        continue  # 如果没有找到院系名称，跳过这个 div

    # 找到所有老师的链接
    teacher_links = department.find_all('a', class_='zhy_tittle')

    for link in teacher_links:
        teacher_name = link.text.strip()
        teacher_url = link['href']

        # 将院系、老师姓名和链接存储到列表中
        data.append({
            'Department': department_name,
            'Teacher': teacher_name.replace(' ', ''),
            'Link': teacher_url
        })

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 打印DataFrame
print(df)
df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')