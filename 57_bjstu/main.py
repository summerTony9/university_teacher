import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://saee.ustb.edu.cn/bcms/act/ListInfo/?classid=145"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)

depts = bs0bj.find_all('div', {'style': "height: auto;overflow: hidden;"})
pre = "https://saee.ustb.edu.cn"
dept_list = []
name_list = []
url_list = []

for dept in depts:
    # print(dept)
    dept_name = dept.find('p')
    dept_name = dept_name.get_text()
    teachers = dept.find_all('li')
    print(teachers)
    for teacher in teachers:
        name = teacher.get_text()
        name = re.sub('[^\u4e00-\u9fa5]+', '', name)
        url = teacher.find('a').get('href')
        url = pre + url
        dept_list.append(dept_name)
        name_list.append(name)
        url_list.append(url)

full_df = pd.DataFrame(
    {'部门': dept_list,
     '姓名': name_list,
     'url': url_list}
)

full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
