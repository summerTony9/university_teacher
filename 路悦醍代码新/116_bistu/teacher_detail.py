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


def extract_info_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    info = {}

    try:
        # 提取姓名、职称和导师信息
        name_tag = soup.find('p', class_='vsbcontent_start').find_next_sibling('p')
        if name_tag:
            info['name'] = name_tag.get_text(strip=True).split(' ')[0]
            info['current_title'] = name_tag.get_text(strip=True).split(' ')[-1]
        else:
            info['name'] = 'N/A'
            info['current_title'] = 'N/A'

        # 提取基本信息
        basic_info_tag = soup.find('h4', text='基本信息').find_next_sibling('p')
        if basic_info_tag:
            basic_info_text = basic_info_tag.get_text(strip=True).split('||')
            for item in basic_info_text:
                if '性别' in item:
                    info['gender'] = item.split('：')[1].strip()
                if '出生年月' in item:
                    info['birthdate'] = item.split('：')[1].strip()
                if '政治面貌' in item:
                    info['political_status'] = item.split('：')[1].strip()
                if '现任职称' in item:
                    info['current_position'] = item.split('：')[1].strip()
        else:
            info.update({'gender': 'N/A', 'birthdate': 'N/A', 'political_status': 'N/A', 'current_position': 'N/A'})

        # 提取最后学历、最后学位、获学位单位信息
        education_info_tag = basic_info_tag.find_next_sibling('p') if basic_info_tag else None
        if education_info_tag:
            education_info_text = education_info_tag.get_text(strip=True).split('||')
            for item in education_info_text:
                if '最后学历' in item:
                    info['highest_education'] = item.split('：')[1].strip()
                if '最后学位' in item:
                    info['highest_degree'] = item.split('：')[1].strip()
                if '获学位单位' in item:
                    info['degree_granting_institution'] = item.split('：')[1].strip()
        else:
            info.update({'highest_education': 'N/A', 'highest_degree': 'N/A', 'degree_granting_institution': 'N/A'})

        # 提取留学信息
        study_abroad_info_tag = education_info_tag.find_next_sibling('p') if education_info_tag else None
        if study_abroad_info_tag:
            study_abroad_info_text = study_abroad_info_tag.get_text(strip=True).split('||')
            for item in study_abroad_info_text:
                if '是否留学' in item:
                    info['study_abroad'] = item.split('：')[1].strip()
                if '留学国别' in item:
                    info['country_of_study'] = item.split('：')[1].strip()
                if '留学时间' in item:
                    info['study_period'] = item.split('：')[1].strip()
        else:
            info.update({'study_abroad': 'N/A', 'country_of_study': 'N/A', 'study_period': 'N/A'})

        # 提取联系方式信息
        contact_info_tag = study_abroad_info_tag.find_next_sibling('p') if study_abroad_info_tag else None
        if contact_info_tag:
            contact_info_text = contact_info_tag.get_text(strip=True).split('||')
            for item in contact_info_text:
                if '邮箱' in item:
                    info['email'] = item.split('：')[1].strip()
                if '通讯地址' in item:
                    info['address'] = item.split('：')[1].strip()
        else:
            info.update({'email': 'N/A', 'address': 'N/A'})

        # 提取所有有标题的信息
        titles = soup.find_all(['h4', 'p'])
        for title in titles:
            title_text = title.get_text(strip=True)
            if title_text in ["基本信息", "导师信息", "所属院系、学科及研究方向", "工作简历", "承担教学任务",
                              "承担的科研项目情况", "论文目录", "科研成果"]:
                content_list = []
                sibling = title.find_next_sibling()
                while sibling and sibling.name in ['p', 'div']:
                    if sibling.name == 'p':
                        content_list.append(sibling.get_text(strip=True))
                    sibling = sibling.find_next_sibling()

                if content_list:
                    info[title_text] = " ".join(content_list)
                else:
                    info[title_text] = 'N/A'
    except Exception as e:
        print(f"Error extracting info: {e}")

    return info

for index in range(len(df)):
    print(index)
    teacher_name = df.loc[index, 'Teacher']
    teacher_url = df.loc[index, 'Link']
    dept = df.loc[index, 'Department']
    # title = df.loc[index, '职称']

    # Extract information
    # try:
    html = requests.get(teacher_url, headers={'User-Agent': UserAgent().random}, verify=False).content
    teacher_info = extract_info_from_html(html)
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
