import re
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd


def extract_info(text):
    cut = ['教育经历', '研究方向', '研究成果', '招生方向', '']
    middle = ['：(.*?)', '：(.*?)', '：(.*?)', '：(.*)']
    # print(under)
    detail_dict = {}
    for index in range(4):
        pattern = r'' + cut[index] + middle[index] + cut[index+1]
        content = re.findall(pattern, text)
        if len(content) > 0:
            print(content)
            content = content[0]
        else:
            content = None
        detail_dict[cut[index]] = content
    return detail_dict


# infos_list = []
info_list = []
for j in range(9):
    if j == 0:
        url = 'https://6y.nuc.edu.cn/gyxy/jzg/jzgyl.htm'
    else:
        url = 'https://6y.nuc.edu.cn/gyxy/jzg/jzgyl/' + str(9-j) + '.htm'
    print(url)

    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, 'html.parser')
    # 获得信息和详情
    infos = bs0bj.find_all('div', {'class': 'media col-xs-6'})
    infos = infos[0:14]
    if j == 0:
        details = bs0bj.find_all('div', {'class': 'modal fade'})

    # 全部的循环，每一次都可以拿到126条信息
    for info in infos:
        # 从基本中拿到基本信息
        items = info.find_all('li')
        target_id = items[0].find('a')['data-target'].replace('#', '')
        teacher_dict = {}
        for item in items:
            key, value = item.get_text().split('：')
            # print(key, value)
            teacher_dict[key] = value

        # 根据序号匹配details
        detail = bs0bj.find('div', {'id': target_id})

        # details 中的学科和信息
        first = detail.find('ul').find_all('li')
        for item in first:
            if '所属学科' in item.get_text():
                teacher_dict['学科'] = item.get_text().replace('所属学科：', '')
            if '所属专业' in item.get_text():
                teacher_dict['专业'] = item.get_text().replace('所属专业：', '')

        # 其他信息（有两种情况）
        under = detail.find('div', id='teacher-dialog-bottom').get_text().replace('\n', '').replace(' ', '').replace(
            '\t', '').replace('\r', '')
        if '教育经历' in under:
            detail_dict = extract_info(under)
            teacher_dict.update(detail_dict)
        else:
            teacher_dict['详细信息'] = under
        info_list.append(teacher_dict)


info_df = pd.DataFrame(info_list)
print(info_df)
info_df.to_csv('teacher_detail.csv', index=False, encoding='utf-8-sig')
