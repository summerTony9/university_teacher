import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


# Department


# Read the HTML file
import random
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

df = pd.read_csv('teacher_info.csv')
print(df.head())

dict_list = []


def get_info(url):
    html = requests.get(url, headers={'User-Agent': UserAgent().random}, verify=False).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    capitions = bs0bj.find_all('h4')

    info_dict = {}


    # Extract information using the defined patterns

    for capition in capitions:
        # Print the capition text
        # print(capition.get_text(strip=True))
        key = capition.get_text(strip=True)
        # Find the next sibling element which is supposed to be the corresponding content
        next_element = capition.find_next_sibling()
        value = ''
        while next_element and next_element.name != 'h4':
            # print(next_element.get_text(strip=True))
            value += next_element.get_text(strip=True).replace('\xa0', '')
            next_element = next_element.find_next_sibling()

        if key == '基本信息':
            parts = value.split('||')

            # Create an empty dictionary to store the extracted information
            # Loop through each part and extract key-value pairs
            for part in parts:
                # Remove any leading/trailing whitespace
                part = part.strip()
                if '：' in part:
                    # Split the part into key and value based on '：'
                    key, value = part.split('：', 1)
                    # Add the key-value pair to the dictionary
                    info_dict[key] = value

        info_dict[key] = value

    return info_dict

for index in range(len(df)):
    print(index)
    teacher_name = df.loc[index, 'Teacher']
    teacher_url = df.loc[index, 'Link']
    dept = df.loc[index, 'Department']
    # title = df.loc[index, '职称']

    # Extract information
    # try:
    html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}, verify=False).content
    teacher_info = get_info(teacher_url)
    # except:
    #     teacher_info = {}

    teacher_info['姓名'] = teacher_name
    teacher_info['系'] = dept
    # teacher_info['职称'] = title
    teacher_info['链接'] = teacher_url
    print(teacher_info)

    dict_list.append(teacher_info)

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
