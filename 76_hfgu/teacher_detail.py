import random
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

df = pd.read_csv('teacher_info.csv')
print(df.head())

result_list = []
error_df = []

for index in range(104, 105):
    time.sleep(random.uniform(3, 5))
    teacher_name = df.loc[index, '姓名']
    teacher_url = df.loc[index, 'url']
    print(teacher_name, index)
    teacher_dict = {'姓名': teacher_name, 'url': teacher_url}

    # try:
    html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    table = bs0bj.find('center').find('tbody')
    rows = table.find_all('tr')

    for row in rows:
        # print(row)
        row_info_list = row.find_all('li')
        if len(row_info_list) == 0:
            key = row.find('td').get_text()
            value = row.find('td').find_next('td').get_text()
            teacher_dict[key] = value.replace('\xa0', '').replace('\r', "")

        else:
            for info in row_info_list:
                print(info)
                key = info.find('div').get_text()
                value = info.find('div').find_next('div').get_text()
                teacher_dict[key] = value.replace('\xa0', '').replace('\r', "")
    result_list.append(teacher_dict)
    # except Exception as e:
    #     print(e)
    #     print(index, teacher_name, teacher_url)
    #     error_df.append({'teacher_name': teacher_name, 'teacher_url': teacher_url})
    #     continue


def merge_dicts_with_list_values(dict_list):
    all_keys = set(key for d in dict_list for key in d.keys())

    # 初始化最终的字典，每个键对应一个空列表
    merged_dict = {key: [] for key in all_keys}

    # 遍历每个字典和所有键
    for key in all_keys:
        for d in dict_list:
            # 如果当前字典有这个键，则添加它的值；否则，添加一个空值
            merged_dict[key].append(d.get(key, None))  # 用None作为空值，也可以用""或其他

    return merged_dict

exit()
result_df = pd.DataFrame(
    merge_dicts_with_list_values(result_list)
)
result_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')

error_df = pd.DataFrame(
    merge_dicts_with_list_values(error_df)
)
error_df.to_csv('error_teacher_detail.csv', index=False, encoding='utf-8-sig')

# result_list.append(teacher_dict
# print(teacher_dict)
