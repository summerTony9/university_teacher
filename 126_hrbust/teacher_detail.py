import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

df = pd.read_csv('teacher_info.csv')
dict_list = []

for index in range(len(df)):
    url = df.loc[index, 'url']
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    tds = bs0bj.find_all('td')
    tds = [
        td for td in tds
        if td.get('rowspan') != '4'
    ]

    tds = [
        td for td in tds
        if td.find('img') is None
    ]

    tds = [
        td for td in tds
        if td.get('align') != 'center'
    ]

    tds = [
        td.get_text().strip().replace(" \xa0", "")
        for td in tds
    ]

    for i in range(1, len(tds), 2):
        if i >= len(tds) - 1:
            break

        if tds[i + 1] == "":
            tds.pop(i + 1)
            break

    # tds = [td for td in tds if td != '']
    info_dict = {}
    is_info = False

    for i in range(0, len(tds), 2):
        if tds[i] == "":
            continue
        else:
            key = tds[i].replace(" ", "").replace('\xa0', "")
            if not is_info:
                is_info = key == "姓名"
            if is_info:
                info_dict[key] = tds[i + 1].replace(" ", "").replace('\xa0', "")
    print(info_dict)
    info_dict['姓名'] = df.loc[index, '姓名']
    info_dict['链接'] = url
    info_dict['院系'] = df.loc[index, 'dept_name']

    dict_list.append(info_dict)


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
    if not_missing <= 2:
        result_df.drop(columns=col, inplace=True)

result_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')
