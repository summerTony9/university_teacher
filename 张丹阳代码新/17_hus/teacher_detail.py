import random
import re
import time

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

df = pd.read_csv('teacher_info.csv')
dict_list = []

for index in range(len(df)):
    # index = 30
    url = df.loc[index, 'url']
    print(url)
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    # print(bs0bj.prettify())
    try:
        js_data = bs0bj.find('div', {'class': 'js_data'})
        title = js_data.find('span').find_next('span').get_text().strip()
        info_dict = {'title': title}

        top_infos = js_data.find_all('p')
        for info in top_infos:
            key = info.find('span').get_text().strip()
            value = info.find('span').next_sibling
            if value and not isinstance(value, str):
                value = value.next_sibling
            if value is None:
                value = ''
            else:
                value = value.strip()

            key = key.replace('\u3000', '')
            # print(key, value)
            info_dict[key] = value

        js_xxs = bs0bj.find_all('div', {'class': 'js_xx'})
        for info in js_xxs:
            key = info.find('h6').get_text().strip()
            value = info.find('textarea').get_text().strip()
            info_dict[key] = value

        info_dict['姓名'] = df.loc[index, '姓名']

    except AttributeError:
        info_dict = {'姓名': df.loc[index, '姓名']}

    dict_list.append(info_dict)
    time.sleep(random.randint(1, 3))


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
