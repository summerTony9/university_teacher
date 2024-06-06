import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

url = 'https://www.tju.edu.cn/rcpy/szdw/lyys.htm'
html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
soup = BeautifulSoup(html, 'html.parser')

dict_list = []
infos = soup.find('div', {'class': 'list_xsqk'}).find_all('li')
info_dict = {
        '姓名': [],
        'title': [],
        'detail': []
    }
for info in infos:
    name = info.find('h2').get_text()

    # 分割点
    # split_point = "院士"
    #
    # # 在分割点分割字符串，并包含分割点在第一个字段中
    # title, name = text.split(split_point)
    # field1 = parts[0] + split_point
    # field2 = parts[1]
    title = re.match(".*院士", name).group()
    name = name.replace(title, '').replace('教授', '')
    print(name)
    detail = info.find('p').get_text()
    print(detail)
    # dict_list.append(pd.DataFrame({
    #     '姓名': [name],
    #     'title': [title],
    #     'detail': [detail]
    # }))
    info_dict['姓名'].append(name)
    info_dict['title'].append(title)
    info_dict['detail'].append(detail)

df = pd.DataFrame(info_dict)
# full_df = pd.concat(dict_list)
df.to_csv('teacher.csv', index=False, encoding='utf-8-sig')

