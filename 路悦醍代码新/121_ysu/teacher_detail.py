from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

index = 0
df = pd.read_csv("teacher_info.csv")
url = df['url'][index]

html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

info_dict = {}

teacher_info = bs0bj.find('div', {'class': 'teacher_mid_topLinpro fl'})
name = teacher_info.find('span').get_text()
info_dict['姓名'] = name

info_list = teacher_info.find_all('li')
for info in info_list:
    text = info.get_text()
    if '：' not in text:
        key = '职位'
        value = text
    else:
        key, value = text.split('：', 1)
    info_dict[key] = value

side_bar = bs0bj.find('div', {'class': 'teacher_mid_topRin fl'})
side_bar = side_bar.get_text().replace(" ", '')
side_bar = side_bar.split('\n')
side_bar = [x for x in side_bar if x != '']
for info in side_bar:
    print(info)
    key, value = info.split(':', 1)
    if key == '电子信箱':
        data = {
            'id': "_tsites_encryp_tsteacher_tsemail",
            'content': value,
            'mode': '8'
        }
        value = requests.get("http://web.ysu.edu.cn/system/resource/tsites/tsitesencrypt.jsp", params=data).text
    info_dict[key] = value
print(info_dict)
