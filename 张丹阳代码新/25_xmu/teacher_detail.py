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

    teacher_title = bs0bj.find('div', {'class': 'teacher-title'}).find_all('p')
    teacher_title = [title.get_text().strip() for title in teacher_title]
    teacher_title = {title.split('：')[0]: title.split('：')[1] for title in teacher_title}

    teacher_resumes = bs0bj.find_all('div', {'class': 'teacherResume'})
    info_dict = {}
    print(teacher_resumes)
    for teacher_resume in teacher_resumes:
        h3 = teacher_resume.find('h3')
        h3 = h3.get_text().strip().replace('：', '').replace(':', '')
        if h3 != '个人简历':
            value = teacher_resume.find('p').get_text().strip()
            info_dict[h3] = value
        else:
            contents = teacher_resume.find('div', {'class': 'wp_articlecontent'})
            if contents is None:
                continue
            br_tags = contents.find_all('br')


            # Function to find the topmost parent of a tag until 'div' is reached
            def find_topmost_parent(tag, stop_tag_name='div'):
                parent = tag
                while parent.parent and parent.parent.name != stop_tag_name:
                    parent = parent.parent
                return parent


            # Initialize list to store sections of interest
            sections = []

            # Step 1: Extract content before the first <br>
            if br_tags:
                first_br = br_tags[0]
                content_before_first_br = []
                current_element = find_topmost_parent(first_br).previous_sibling
                while current_element:
                    if not isinstance(current_element, str) or current_element.strip():
                        content_before_first_br.insert(0, current_element)
                    current_element = current_element.previous_sibling
                sections.append(content_before_first_br)

            # Step 2: Extract content between each pair of <br> tags
            for i in range(len(br_tags) - 1):
                first_br = br_tags[i]
                second_br = br_tags[i + 1]

                first_br_parent = find_topmost_parent(first_br)
                second_br_parent = find_topmost_parent(second_br)

                current_element = first_br_parent.next_sibling
                elements_between_brs = []
                while current_element and current_element != second_br_parent:
                    if not isinstance(current_element, str) or current_element.strip():
                        elements_between_brs.append(current_element)
                    current_element = current_element.next_sibling

                sections.append(elements_between_brs)

            # Step 3: Extract content after the last <br>
            if br_tags:
                last_br = br_tags[-1]
                content_after_last_br = []
                current_element = find_topmost_parent(last_br, 'p').next_sibling
                while current_element:
                    if not isinstance(current_element, str) or current_element.strip():
                        content_after_last_br.append(current_element)
                    current_element = current_element.next_sibling

                sections.append(content_after_last_br)

            for idx, section in enumerate(sections):
                flag = 0
                print(f"Section {idx}:")
                print(section)
                if len(section) >= 2:
                    key_index = 0
                    key = section[key_index].get_text().strip().replace('：', '').replace(':', '')
                    while key == '':
                        key_index += 1
                        if key_index >= len(section):
                            flag = 1
                            break
                        key = section[key_index].get_text().strip().replace('：', '').replace(':', '')
                    if flag == 1:
                        continue
                    for i in ['一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、']:
                        key = key.replace(i, '')
                    if key not in info_dict.keys() and len(key) < 20:
                        value = ''.join([e.get_text() for e in section[1:]])
                        info_dict[key] = value.replace('\n', '').replace('\r', ''
                                                                         ).replace('\t', '').replace(
                            '\xa0', '')

            print(info_dict)
    total_info = {**teacher_title, **info_dict}
    total_info['姓名'] = df.loc[index, '姓名']
    total_info['链接'] = url
    dict_list.append(total_info)


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
