from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://sise.zstu.edu.cn/szdw1/zgjzc.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)

infos = bs0bj.find('ul', {'class': 'list'}).find_all('li')
pre = "https://sise.zstu.edu.cn/"
names = []
urls = []
title = []


def tidy_url(url):
    if 'http' in url:
        return url
    else:
        return pre + url[3:]


for info in infos:
    name = info.get_text().replace("\n", "")
    href = info.find('a').get('href')
    url = tidy_url(href)
    names.append(name)
    urls.append(url)
    title.append("正高级职称")

base_url = "https://sise.zstu.edu.cn/szdw1/fgjzc.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)

infos = bs0bj.find('ul', {'class': 'list'}).find_all('li')
pre = "https://sise.zstu.edu.cn/"

for info in infos:
    name = info.get_text().replace("\n", "")
    href = info.find('a').get('href')
    url = tidy_url(href)
    names.append(name)
    urls.append(url)
    title.append("副高级职称")

full_df = pd.DataFrame(
    {'姓名': names,
     'url': urls,
     '职称': title}
)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
