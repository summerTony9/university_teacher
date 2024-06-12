import re
import time

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

# url = "http://dscx.yjs.nchu.edu.cn/homepage/376.html"

dict_list = []
df = pd.read_csv('teacher_info.csv')
df = df.drop_duplicates(subset=['姓名'], ignore_index=True)
print(df)

for i in range(len(df)):
    url = df['url'][i]
    print(url)
    # url = "http://dscx.yjs.nchu.edu.cn/homepage/288.html"
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    capitions = bs0bj.find_all(class_='js-capition')

    info_dict = {}

    patterns = {
        "姓名": "姓名：(.*?)性别",
        "性别": "性别：(.*?)在岗性质",
        "在岗性质": "在岗性质：(.*?)最高学位",
        "最高学位": "最高学位：(.*?)专业技术职务",
        "专业技术职务": "专业技术职务：(.*?)毕业学校",
        "毕业学校": "毕业学校：(.*?)行政职务",
        "行政职务": "行政职务：(.*?)所在院校",
        "所在院校": "所在院校：(.*?)联系电话",
        "联系电话": "联系电话：(.*?)电子邮箱",
        "电子邮箱": "电子邮箱：(.*?)相册"
    }

    # Extract information using the defined patterns

    for capition in capitions:
        # Print the capition text
        print(capition.get_text(strip=True))
        key = capition.get_text(strip=True)
        info_list = []
        # Find the next sibling element which is supposed to be the corresponding content
        next_element = capition.find_next_sibling()
        value = ''
        while next_element and next_element.get('class') != ['js-capition']:
            print(next_element.get_text(strip=True))
            value += next_element.get_text(strip=True)
            next_element = next_element.find_next_sibling()
        print(key, value)
        if key == '基本信息':
            print(value)
            extracted_info = {field: re.search(pattern, value, re.S).group(1).strip() for field, pattern in
                              patterns.items()
                              if re.search(pattern, value, re.S)}
            print(extracted_info)

            info_dict.update(extracted_info)
        else:
            info_dict[key] = value
    info_dict['url'] = url
    info_dict['姓名'] = df['姓名'][i]
    dict_list.append(info_dict)
    # time.sleep(5)


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
