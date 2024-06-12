import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

df = pd.read_csv('teacher_info.csv')
dict_list = []
for index in range(len(df)):
    # index = 15
    url = df.loc[index, 'url']
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    teacher_info_top = bs0bj.find('div', {'class': 'teacher-info-top'})
    try:
        zc = teacher_info_top.find('div', {'class': 'teacher-field zc'}).get_text().strip()
    except AttributeError:
        zc = None
    dh = teacher_info_top.find_all('div', {'class': 'teacher-field dh'})
    dh = [item.find_all('span') for item in dh]
    dh = [item.get_text().strip() for sublist in dh for item in sublist]
    dh_dict = [item.split('：') for item in dh]
    dh_dict = {item[0]: item[1] for item in dh_dict}
    top_dict = {'职称': zc, **dh_dict}
    print(top_dict)

    item_dict = {}
    teacher_items = bs0bj.find('ul', {'class': 'teacher-nav clearfix'}).find_all('li')
    teacher_items = [item.get_text().strip() for item in teacher_items]
    teacher_item_index = 1

    teacher_fields = bs0bj.select('div.teacher-field:not(.title):not(.zc):not(.dh)')
    for field in teacher_fields:
        tit = field.find('div', {'class': 'tit'})
        if tit is not None:
            field_name = field.find('div', {'class': 'tit'}).get_text().strip()
            field_value = field.find_all('div', {'class': 'con'})
            field_value = ''.join(
                [item.get_text() for item in field_value]
            )
        else:
            field_name = teacher_items[teacher_item_index]
            field_value = field.get_text()
            teacher_item_index += 1

        item_dict[field_name] = field_value

    item_dict['姓名'] = df.loc[index, '姓名']
    item_dict['title'] = df.loc[index, 'title']

    dict_list.append({**top_dict, **item_dict})

def merge_dicts_with_list_values(dict_list):
    # 确定所有字典中所有唯一键的集合
    all_keys = set(key for d in dict_list for key in d.keys())

    # 初始化最终的字典，每个键对应一个空列表
    merged_dict = {key: [] for key in all_keys}

    # 遍历每个字典和所有键
    for key in all_keys:
        for d in dict_list:
            # 如果当前字典有这个键，则添加它的值；否则，添加一个空值
            merged_dict[key].append(d.get(key, None))  # 用None作为空值，也可以用""或其他

    return merged_dict


result_df = pd.DataFrame(
    merge_dicts_with_list_values(dict_list)
)

for col in result_df.columns:
    not_missing = result_df[col].notnull().sum()
    if not_missing <= 3:
        result_df.drop(columns=col, inplace=True)

result_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')


