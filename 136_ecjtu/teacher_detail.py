from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
from functions import merge_dicts_with_list_values, replace_all

df = pd.read_csv('teacher_info.csv')
print(df.head())

error_df = []

result_list = []
for index in range(len(df)):
    teacher_name = df.loc[index, 'teacher_name']
    teacher_url = df.loc[index, 'teacher_url']
    html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    teacher_info = bs0bj.find('div', {'class': 'v_news_content'}).find_all('p')
    teacher_info = [info.get_text() for info in teacher_info if info.get_text() != '']
    replace_dict = {'\xa0': '', ' ': '', '\n': '', '\u200d': '', '\r': ''}
    teacher_info = [replace_all(info, replace_dict) for info in teacher_info]
    teacher_info = [info for info in teacher_info if info != '']
    result_dict = {}
    extra_info = ""
    try:
        for info in teacher_info:
            if '：' in info:
                key, value = info.replace('\n', '').split('：', 1)
                if len(key) > 20 or any(char.isdigit() for char in key):
                    key = 'extra_info'
                    extra_info += info
                    value = extra_info
            else:
                key = 'extra_info'
                extra_info += info
                value = extra_info
            if value != '':
                result_dict[key] = value
        result_dict['姓名'] = teacher_name
        result_dict['链接'] = teacher_url
        result_dict['院系'] = df.loc[index, 'department']
        result_list.append(result_dict)
    except ValueError:
        print(index, teacher_name, teacher_url)
        print(teacher_info)
        error_df.append({'teacher_name': teacher_name, 'teacher_url': teacher_url})
        continue

result_df = pd.DataFrame(
    merge_dicts_with_list_values(result_list)
)
result_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')

error_df = pd.DataFrame(
    merge_dicts_with_list_values(error_df)
)
error_df.to_csv('error_teacher_detail.csv', index=False, encoding='utf-8-sig')

