import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

url_base = [
    "https://dkxy.xust.edu.cn/szdw/sssds.htm",
    "https://dkxy.xust.edu.cn/szdw/sssds/3.htm",
    "https://dkxy.xust.edu.cn/szdw/sssds/2.htm",
    "https://dkxy.xust.edu.cn/szdw/sssds/1.htm",
]


def get_info_detail(url):
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    infos = bs0bj.find('div', {'class': "v_news_content"})
    return infos.get_text().strip()


def get_info(base_url):
    html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    # print(bs0bj.contents)

    infos = bs0bj.find('ul', {'class': "list-leader"}).find_all('li')

    names = []
    urls = []
    info_list = []

    for info in infos:
        name = info.get_text().strip()
        url = info.find('a').get('href')
        url = "https://dkxy.xust.edu.cn/" + url[3:]
        names.append(name)
        urls.append(url)
        info_list.append(get_info_detail(url))

    return pd.DataFrame(
        {'姓名': names,
         'url': urls,
         '信息': info_list}
    )


df_list = [get_info(url) for url in url_base]
result = pd.concat(df_list, ignore_index=True)
result.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
