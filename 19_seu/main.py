# read json file
import json

import pandas as pd


with open('data.json', 'r') as f:
    file_data = json.load(f)

data = file_data['data']
name_list = []
url_list = []
kind_list = []

for item in data:
    name_list.append(item['title'])
    url_list.append(item['cnUrl'])
    kind_list.append(item['exField1'])


df = pd.DataFrame(
    {'姓名': name_list,
     'url': url_list,
     'title': kind_list}
)

df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
