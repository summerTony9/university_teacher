import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


def extract_teacher_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    teacher_info = {}

    # Extracting basic information
    basic_info_section = soup.find('div', class_='t_jbxx_nr')
    if basic_info_section:
        paragraphs = basic_info_section.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if '性别' in text:
                teacher_info['性别'] = text.split(':')[-1].strip()
            elif '出生年月' in text:
                teacher_info['出生年月'] = text.split(':')[-1].strip()
            elif '毕业院校' in text:
                teacher_info['毕业院校'] = text.split(':')[-1].strip()
            elif '学历' in text:
                teacher_info['学历'] = text.split(':')[-1].strip()
            elif '学位' in text:
                teacher_info['学位'] = text.split(':')[-1].strip()
            elif '所在单位' in text:
                teacher_info['所在单位'] = text.split(':')[-1].strip()
            elif '办公地点' in text:
                teacher_info['办公地点'] = text.split(':')[-1].strip()
            elif 'Email' in text:
                teacher_info['Email'] = text.split(':')[-1].strip()
            else:
                key_value = text.split('：')
                if len(key_value) == 2:
                    teacher_info[key_value[0].strip()] = key_value[1].strip()

    # Check for alternative basic info layout
    alternative_basic_info = soup.find_all('li')
    for li in alternative_basic_info:
        text = li.get_text(strip=True)
        if '性别' in text:
            teacher_info['性别'] = text.split(':')[-1].strip()
        elif '出生年月' in text:
            teacher_info['出生年月'] = text.split(':')[-1].strip()
        elif '毕业院校' in text:
            teacher_info['毕业院校'] = text.split(':')[-1].strip()
        elif '学历' in text:
            teacher_info['学历'] = text.split(':')[-1].strip()
        elif '学位' in text:
            teacher_info['学位'] = text.split(':')[-1].strip()
        elif '所在单位' in text:
            teacher_info['所在单位'] = text.split(':')[-1].strip()
        elif '办公地点' in text:
            teacher_info['办公地点'] = text.split(':')[-1].strip()
        elif 'Email' in text:
            teacher_info['Email'] = text.split(':')[-1].strip()

    # Extracting personal profile
    profile_section = soup.find('div', class_='t_grjj_nr') or soup.find('div', class_='CurrencyBox', text='个人简介')
    if profile_section:
        teacher_info['个人简介'] = profile_section.get_text(strip=True)

    # Extracting education background
    education_section = soup.find('div', class_='bd') or soup.find('div', class_='CurrencyBox', text='教育经历')
    education_list = []
    if education_section:
        education_items = education_section.find_all('ul')
        for item in education_items:
            education = {}
            dates = item.find_previous('div', class_='t_e_date').get_text(strip=True) if item.find_previous('div',
                                                                                                            class_='t_e_date') else None
            education['时间'] = dates
            li_elements = item.find_all('li')
            if len(li_elements) >= 4:
                education['学校'] = li_elements[0].get_text(strip=True)
                education['专业'] = li_elements[1].get_text(strip=True)
                education['学历'] = li_elements[2].get_text(strip=True)
                education['学位'] = li_elements[3].get_text(strip=True)
            else:
                education['内容'] = li_elements[0].get_text(strip=True)
            education_list.append(education)
        teacher_info['教育经历'] = education_list

    # Extracting work experience
    work_experience_section = soup.find('div', class_='CurrencyBox', text='工作经历')
    work_experience_list = []
    if work_experience_section:
        work_experience_items = work_experience_section.find_all('li')
        for item in work_experience_items:
            work_experience = {}
            dates = item.find('p').get_text(strip=True) if item.find('p') else None
            work_experience['时间'] = dates
            li_elements = item.find_all('li')
            if len(li_elements) >= 3:
                work_experience['单位'] = li_elements[0].get_text(strip=True)
                work_experience['职位'] = li_elements[1].get_text(strip=True)
            work_experience_list.append(work_experience)
        teacher_info['工作经历'] = work_experience_list

    return teacher_info


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

for index in range(len(df)):
    print(index)
    teacher_name = df.loc[index, '姓名']
    teacher_url = df.loc[index, '链接']
    dept = df.loc[index, '系']
    title = df.loc[index, '职称']

    # Extract information
    try:
        html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}).content
        teacher_info = extract_teacher_info(html)
    except:
        teacher_info = {}

    teacher_info['姓名'] = teacher_name
    teacher_info['系'] = dept
    teacher_info['职称'] = title
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
