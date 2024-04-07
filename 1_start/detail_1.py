import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import openpyxl


def extract_info(infos):
    ret = {}
    targets = ['电话', 'E-mail', '教育背景', '工作履历', '研究领域', '研究概况']
    for info in infos:
        info = info.get_text().replace('　', '')
        # print(info)
        for target in targets:
            if target in info:
                temp = info.replace(target, '').strip().strip('：')
                ret[target] = re.sub(r'\n+', '\n', temp)

    return ret


teacher_info = pd.read_csv('teacher_info.csv')
teacher_details_list = []
error_index = []

index = 0

for index in (range(len(teacher_info))):
    try:
        url = teacher_info['link'][index]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 拿到基本信息
        info = soup.find('div', class_='title')

        name = teacher_info['姓名'][index]
        span_list = info.find_all('span')
        title = span_list[1].get_text()
        organization = info.find('h4').get_text()
        details = info.find_all('p')
        detail_dict = extract_info(details)
        # telephone = detail_dict['电话']
        # mail = detail_dict['E-mail']

        # 更多细节
        more_details = []
        details = soup.find_all('div', class_='home home1')
        for detail in details:
            temp = detail.find('div', class_='home home1')
            # print(temp)
            if temp is not None:
                more_details.append(temp)
        details = soup.find_all('div', class_='home home2')
        more_details = [x for x in more_details] + [x for x in details]

        main_details = extract_info(more_details)

        # 得到新的结果
        teacher_details_list.append(pd.DataFrame({
            '姓名': [name],
            '职称': [teacher_info['级别'][index]],
            '称号': [title],
            '机构': [organization],
            '电话': [detail_dict['电话']],
            '邮箱': [detail_dict['E-mail']],
            '教育背景': [main_details['教育背景']],
            '工作履历': [main_details['工作履历']],
            '研究领域': [main_details['研究领域']],
            '研究概况': [main_details['研究概况']]
        }))

        teacher_details = pd.concat(teacher_details_list)
        teacher_details.to_excel('output_V0\\output{}.xlsx'.format(index),index = False)

        print(index, name)
    except Exception as e:
        error_index.append(pd.DataFrame({
            '序号': [index],
            'name': [teacher_info['姓名'][index]],
            'url': [teacher_info['link'][index]]
        }))
        print('error'+str(index)+teacher_info['姓名'][index])
        error_pd = pd.concat(error_index)
        error_pd.to_excel('error.xlsx',index=False)




