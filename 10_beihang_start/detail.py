import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


def extract_address(addrs):
    addr_info = {}
    for i in range(len(addrs)):
        if i == 0:
            addr_info['title'] = addrs[i].get_text()
        else:
            targets = ['出生年月', '办公电话', '办公地址', '邮箱']
            addr = addrs[i].get_text()
            for target in targets:
                if target in addr:
                    addr_new = addr.replace(target, '').replace("：", '').strip()
                    if addr_new != '/':
                        addr_info[target] = addr_new
    return addr_info

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


teacher_info = pd.read_csv('teacher_info.csv')
dict_list = []

for i in range(len(teacher_info)):
    # url = 'https://yqgdxy.buaa.edu.cn/info/1017/5226.htm'
    url = teacher_info.loc[i, 'url']
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, 'html.parser')

    details = bs0bj.find('div', {'class': 'teacher-p'}).find('div', {'class': 'col-xs-6'}).find_all('p')
    more_info = bs0bj.find('div', {'class': 'v_news_content'})
    info = extract_address(details)
    info['url'] = url
    info['姓名'] = teacher_info.loc[i, '姓名']
    info['研究室'] = teacher_info.loc[i, '研究室']
    info['详细信息'] = more_info.get_text()
    dict_list.append(info)


result_df = pd.DataFrame(
    merge_dicts_with_list_values(dict_list)
)

result_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')

