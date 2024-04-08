from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

home_url = "https://me.ecjtu.edu.cn/szdw1/jxsjjcb1.htm"
base_url = "https://me.ecjtu.edu.cn/szdw1/"
html = requests.get(home_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

side_menu = bs0bj.find('div', {'class': 'sideMenu'})
dept_info = side_menu.find_all('a')
dept_urls = [url['href'] for url in dept_info]
dept_urls = [base_url + url for url in dept_urls]
dept_names = [url.get_text() for url in dept_info]

# combine the department names and urls
dept_dict = dict(zip(dept_names, dept_urls))
print(dept_dict)
teacher_name_list = []
teacher_url_list = []
dept_list = []

for dept_name, dept_url in dept_dict.items():
    html = requests.get(dept_url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    teacher_info = bs0bj.find(
        'li', {'class': 'cleafix'}).find_all('div', {'class': 'list-con'})
    teacher_urls = [info.find('a')['href'] for info in teacher_info]
    teacher_urls = ["https://me.ecjtu.edu.cn/" + url[2:] for url in teacher_urls]
    teacher_names = [info.get_text().replace('\n', '') for info in teacher_info]

    teacher_name_list.extend(teacher_names)
    teacher_url_list.extend(teacher_urls)
    dept_list.extend([dept_name] * len(teacher_names))

pd.DataFrame(
    {'teacher_name': teacher_name_list,
     'department': dept_list,
     'teacher_url': teacher_url_list}).to_csv(
    'teacher_info.csv', index=False, encoding='utf-8-sig')
