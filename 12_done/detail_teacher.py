from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd
import re

teacher_info_pd = pd.read_csv('teacher_info.csv')
print(teacher_info_pd.head())

for index in range(teacher_info_pd.shape[0]):
    try:
        # index = 0
        url = teacher_info_pd['url'][index]
        # print(url)
        html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
        bs0bj = BeautifulSoup(html, features='html.parser')
        # print(bs0bj.prettify())

        title = bs0bj.find('div', {'class': 'tips'}).get_text()
        # print(title)

        # 联系方式
        contact = bs0bj.find('div', {'class': 'cont'})
        contact = contact.find_all('p')
        contact = [c.get_text() for c in contact]
        # print(contact)

        basic_info = bs0bj.find('li')
        # print(basic_info.get_text())

        teacher_id = bs0bj.find('div', {"class": "col-l teacher-body"}).get('data-tid')
        # print(teacher_id)
        req = requests.post("https://homepage.hit.edu.cn/TeacherHome/teacherBody.do", data={'id': teacher_id})
        bs0bj = BeautifulSoup(req.content, features='html.parser')

        teacher_name = teacher_info_pd['name'][index]
        info = bs0bj.find_all('li')


        # for i in info:
        #     print(i.text)
        #     print("---------------------------------")

        def tidy_text(text, text_name):
            return text.replace(" ", "").replace(text_name, "").replace("名称", "")


        def extract_info(infos):
            ret = {}
            targets = ['基本信息', '学术兼职', '奖励与荣誉', '招生信息', '工作经历', '教育经历 ', '研究领域',
                       ' 团队成员 ', '已毕业研究生', '指导本科毕业设计', '代表论文']
            for info in infos:
                info = info.get_text()
                for target in targets:
                    if target in info:
                        ret[target] = tidy_text(info, target)
            return ret


        ans = extract_info(info)
        # print(extract_info(info))
    except Exception as e:
        print(teacher_name)
        continue
