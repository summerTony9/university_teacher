import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

df = pd.read_csv('teacher_info.csv')
dict_list = []
for index in range(len(df)):
    # index = 1
    url = df.loc[index, 'url']
    name = df.loc[index, '姓名']
    teacher_dict = {}
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    try:
        mail = bs0bj.find('div', {'id': 'vsb_content'}).find('tr').find_next('tr').get_text().strip()
        # get the email address
        mail = mail.replace('Email：', '')
        teacher_dict['email'] = mail
    except AttributeError:
        mail = ''
        teacher_dict['email'] = mail
    print(mail)

    try:
        teacher_title = bs0bj.find('span', string=name)
        teacher_title = teacher_title.find_next('p').get_text()
        teacher_dict['title'] = teacher_title
        print(teacher_title)
    except AttributeError:
        teacher_title = ''
        teacher_dict['title'] = teacher_title
        print(teacher_title)

    def get_detail_resume(resume_url):
        return_dict = {}
        # resume_url = detail_resume
        html = requests.get(resume_url, headers={'User-Agent': UserAgent().random}).content
        bs0bj = BeautifulSoup(html, features='html.parser')
        cards = bs0bj.find_all("div", {'class': 'portlet-content'})
        for card in cards:
            try:
                card_title = card.find('h2', {'class': 'portlet-title-text'}).get_text().strip()
                card_body = card.find('div', {'class': 'portlet-content-container'}).get_text().strip()
                # print(card_title, card_body)
                return_dict[card_title] = card_body
            except AttributeError:
                continue
        return return_dict

    try:
        detail_resume = bs0bj.find('span', string=name).find_parent('a')
    except AttributeError:
        detail_resume = None

    dic = {}
    if detail_resume:
        detail_resume = detail_resume.get('href')
        if detail_resume is not None:
            dic = get_detail_resume(detail_resume)

    teacher_dict.update(dic)
    teacher_dict['姓名'] = name
    teacher_dict['url'] = url
    teacher_dict['dept'] = df.loc[index, 'dept']
    dict_list.append(teacher_dict)


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

    # print(bs0bj.prettify())




