import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_info = {
    'dept_name': ["测控技术与仪器系", "通信工程系", "安全工程系", "电子信息工程系", "电子信息科学与技术系",
                  "光电信息科学与工程系",
                  "电子教研部", "实验中心"],
    'dept_url': [
        "http://cetong.hrbust.edu.cn/744/list.htm",
        "http://cetong.hrbust.edu.cn/745/list.htm",
        "http://cetong.hrbust.edu.cn/746/list.htm",
        "http://cetong.hrbust.edu.cn/dzxxgcx/list.htm",
        "http://cetong.hrbust.edu.cn/dzxxkxyjs/list.htm",
        "http://cetong.hrbust.edu.cn/gdxxkxygc/list.htm",
        "http://cetong.hrbust.edu.cn/cslm/list.htm",
        "http://cetong.hrbust.edu.cn/748/list.htm",
    ],
    'pages': [3, 2, 2, 2, 1, 1, 1, 1]
}


def get_info(url):
    # url = "http://cetong.hrbust.edu.cn/744/list.htm"
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')

    print(bs0bj.prettify())
    infos = bs0bj.find('ul', {'class': "wp_article_list"}).find_all('li')
    names = [info.find('a').get_text().strip() for info in infos]
    urls = ["http://cetong.hrbust.edu.cn/" + info.find('a').get('href') for info in infos]
    return pd.DataFrame(
        {'姓名': names,
         'url': urls}
    )


df_list = []

for i in range(len(base_info['dept_name'])):
    dept_name = base_info['dept_name'][i]
    dept_url = base_info['dept_url'][i]
    pages = base_info['pages'][i]
    print(dept_name, dept_url, pages)

    for page in range(1, pages + 1):
        if page == 1:
            url = dept_url
        else:
            url = dept_url.replace('list.htm', 'list{}.htm'.format(page))
        df = get_info(url)
        df['dept_name'] = dept_name
        df_list.append(df)

full_df = pd.concat(df_list)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
