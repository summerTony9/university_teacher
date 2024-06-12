import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

# df = pd.read_csv('teacher_info.csv')
df = pd.read_csv('error.csv')
info_list = []
error_list = []


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


for i in range(len(df)):
    dict_list = {}
    url = df.loc[i, 'url']
    print(url)
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, 'html.parser')
    # print(bs0bj)
    body = bs0bj.find('div', {'class': 'v_news_content'})
    infos = body.find('table').find_all('tr')
    dict_list['姓名'] = df.loc[i, '姓名']
    dict_list['url'] = url
    try:
        for info in infos:
            key, value = info.get_text().replace('\n', '').replace('：', ':').split(':', 1)
            dict_list[key] = value
        all_keys = dict_list.keys()

        # 找到所有的 strong 标签
        strong_tags = body.find_all('strong')

        # 提取内容
        content = {}
        for strong_tag in strong_tags:
            section_title = strong_tag.get_text()
            content[section_title] = []
            next_sibling = strong_tag.find_next('p')
            while next_sibling and next_sibling.name == 'p':
                content[section_title].append(next_sibling.get_text())
                next_sibling = next_sibling.find_next_sibling('p')
                if next_sibling and next_sibling.find('strong'):
                    break

        # 打印提取的内容
        for section, texts in content.items():
            # print(f"Section: {section}")
            # for text in texts:
            #     print(f" - {text}")
            if section in all_keys:
                continue
            else:
                dict_list[section] = ''.join(texts)

        info_list.append(dict_list)
    except ValueError as e:
        info_list.append(dict_list)
        error_list.append(pd.DataFrame({
            '姓名': [df.loc[i, '姓名']],
            'url': url
        }))

info_dict = merge_dicts_with_list_values(info_list)

result_df = pd.DataFrame(info_dict)
# colnames = result_df.columns.tolist()
# sorted_colnames = sorted(colnames, key=lambda x: result_df[x].notnull().sum())

for col in result_df.columns:
    not_missing = result_df[col].notnull().sum()
    if not_missing <= 3:
        result_df.drop(columns=col, inplace=True)

result_df.to_csv('teacher_detail1.csv', index=False, encoding='utf-8-sig')

error_df = pd.concat(error_list)
error_df.to_csv('error1.csv', index=False, encoding='utf-8-sig')