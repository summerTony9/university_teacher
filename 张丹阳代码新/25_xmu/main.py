import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_info = {
    'title': ["教授", "副教授", "助理教授", "兼职/客座教授"],
    'dept_url': [
        "https://iee.xmu.edu.cn/13309/list.htm",
        "https://iee.xmu.edu.cn/13310/list.htm",
        "https://iee.xmu.edu.cn/13311/list.htm",
        "https://iee.xmu.edu.cn/jzjs/list.htm",
        # "http://cetong.hrbust.edu.cn/dzxxkxyjs/list.htm",
        # "http://cetong.hrbust.edu.cn/gdxxkxygc/list.htm",
        # "http://cetong.hrbust.edu.cn/cslm/list.htm",
        # "http://cetong.hrbust.edu.cn/748/list.htm",
    ],
    'pages': [2, 2, 1, 1]
}


def get_info(url):
    # url = "http://cetong.hrbust.edu.cn/744/list.htm"
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    #
    # print(bs0bj.prettify())
    # exit()
    infos = bs0bj.find('div', {'id': "wp_news_w8"}).find_all('a')
    infos = [info for info in infos if info.find('img') is None]
    names = [info.get_text().strip() for info in infos]
    urls = ["https://iee.xmu.edu.cn/" + info.get('href') for info in infos]
    return pd.DataFrame(
        {'姓名': names,
         'url': urls}
    )


df_list = []

for i in range(len(base_info['title'])):
    title = base_info['title'][i]
    dept_url = base_info['dept_url'][i]
    pages = base_info['pages'][i]
    for page in range(1, pages + 1):
        if page == 1:
            url = dept_url
        else:
            url = dept_url.replace('list.htm', 'list{}.htm'.format(page))
        df = get_info(url)
        df['title'] = title
        df_list.append(df)

full_df = pd.concat(df_list)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
