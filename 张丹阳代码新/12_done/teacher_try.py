import pandas as pd
from bs4 import BeautifulSoup
import requests
# import openpyxl

teacher_info_pd = pd.read_csv('teacher_info.csv')


def tidy_text(text, text_name):
    if text_name != '邮箱':
        return text.replace(" ", "").replace(text_name, "").replace("名称", "")
    else:
        return text.replace(" ", "").replace(text_name, "").replace("名称", "")[::-1] # 反转顺序


def extract_info(infos):
    ret = {}
    targets = ['基本信息', '学术兼职', '奖励与荣誉', '招生信息', '工作经历', '教育经历', '研究领域',
               '团队成员', '已毕业研究生', '指导本科毕业设计', '论文']
    for info in infos:
        info = info.get_text()
        for target in targets:
            if target in info:
                ret[target] = tidy_text(info, target)

    return ret


def extract_address(addrs):
    addr_info = {}
    for addr in addrs:
        targets = ['电话', '传真', '邮箱', '地址']
        addr = addr.get_text()
        for target in targets:
            if target in addr:
                addr_info[target] = tidy_text(addr, target)
    return addr_info


df_basic_list = []
targets = ['基本信息', '学术兼职', '奖励与荣誉', '招生信息', '工作经历', '教育经历', '研究领域',
           '团队成员', '已毕业研究生', '指导本科毕业设计', '论文']

dfs_list = [[] for _ in range(len(targets))]

error_index = []
for index in range(len(teacher_info_pd)):
    try:
        print(index)
        url = teacher_info_pd['url'][index]
        request = requests.get(url)
        request.content.decode('utf-8')
        soup = BeautifulSoup(request.content, 'html.parser')
        print('first soup')
        name = soup.find('h3', class_='tit chineseName').get_text()
        country = soup.find('em', class_='user-country').get_text()
        title = soup.find('div', class_='tips').get_text()
        part = soup.find('div', class_='part2 part').get_text().replace(' ', '')
        position = soup.find('span', class_='user-position').get_text()
        position_url = soup.find('div', class_='part4 part').find('a').get('href')  # 目前就职
        # position_url
        discipline = soup.find('span', class_='user-discipline').get_text()  # 学科
        label = soup.find('span', class_='user-label').get_text()  # 研究方向
        body_id = soup.find('div', class_='col-l teacher-body').get('data-tid')
        # body_id
        is_teacher = requests.post("https://homepage.hit.edu.cn/TeacherHome/isTeacherUser.do", data={'userid': body_id})
        print('is_teacher')
        modify_time = is_teacher.json().get('mDate')
        # soup_is = BeautifulSoup(is_teacher, 'html.parser')
        teacher_body = requests.post(url="https://homepage.hit.edu.cn/TeacherHome/teacherBody.do", data={'id': body_id})
        print('teacher_body')
        soup_body = BeautifulSoup(teacher_body.content, 'html.parser')
        # print(teacher_body.content.decode('utf-8'))
        body_info = soup_body.find_all('li')
        extract_body_info = extract_info(body_info)
        # extract_info.get('基本信息', '')

        addrs = soup.find_all('li', class_='addr')
        addr_info = extract_address(addrs)
        df_basic_list.append(pd.DataFrame({
            '姓名': [name],
            '国家': [country],
            '职称': [title],
            '类型': [part],
            '学院': [position],
            '学院官网': [position_url],
            '学科': [discipline],
            '研究方向': [label],
            '最后修改时间': [modify_time],
            '电话': [addr_info['电话']],
            '传真': [addr_info['传真']],
            '邮箱': [addr_info['邮箱']],
            '地址': [addr_info['地址']]
        }))
        # 针对不同地sheet，生成不同的list?大概是这个思路
        for i in range(len(targets)):
            dfs_list[i].append(pd.DataFrame({
                '姓名': [name],
                'url': [teacher_info_pd['url'][index]],
                targets[i]: [extract_body_info.get(targets[i],'')]
            }))
    except Exception as e:
        error_index.append(pd.DataFrame({
            '序号': [index],
            'name': [teacher_info_pd['name'][index]],
            'url': [teacher_info_pd['url'][index]]
        }))
        print(index, teacher_info_pd['name'][index], teacher_info_pd['url'][index])

    df_basic = pd.concat(df_basic_list)
    dfs = [pd.concat(df) for df in dfs_list]
    if len(error_index) == 0:
        error = pd.DataFrame()
    else:
        error = pd.concat(error_index)

    with pd.ExcelWriter('output{}.xlsx'.format(index)) as writer:
        df_basic.to_excel(writer, index=False, sheet_name='Sheet_name_1')
        for i in range(len(dfs)):
            dfs[i].to_excel(writer, index=False, sheet_name=targets[i])
        error.to_excel(writer, index=False, sheet_name='error')


# df_basic = pd.concat(df_basic_list)
# dfs = [pd.concat(df) for df in dfs_list]
# if len(error_index) == 0:
#     error_index = pd.DataFrame()
# else:
#     error_index = pd.concat(error_index)
#
# with pd.ExcelWriter('output.xlsx') as writer:
#     df_basic.to_excel(writer, sheet_name='Sheet_name_1')
#     for i in range(len(dfs)):
#         dfs[i].to_excel(writer, sheet_name=targets[i])
#     error_index.to_excel(writer, sheet_name='error')
