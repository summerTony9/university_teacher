import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_info = {
    'dept': ["电器工程及其自动化", "自动化系", "测控技术与仪器系", "能源与动力工程系", "实验中心"],
    'dept_url': [
        "http://ee.gzu.edu.cn/3595/list.htm",
        "http://ee.gzu.edu.cn/3597/list.htm",
        "http://ee.gzu.edu.cn/3598/list.htm",
        "http://ee.gzu.edu.cn/3599/list.htm",
        "http://ee.gzu.edu.cn/3602/list.htm"
        # "http://cetong.hrbust.edu.cn/dzxxkxyjs/list.htm",
        # "http://cetong.hrbust.edu.cn/gdxxkxygc/list.htm",
        # "http://cetong.hrbust.edu.cn/cslm/list.htm",
        # "http://cetong.hrbust.edu.cn/748/list.htm",
    ],
    'pages': [2, 1, 1, 1, 1]
}


# url = "http://ee.gzu.edu.cn/3595/list.htm"

def get_content(url):
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    content = bs0bj.find('div', {'class': "Article_Content"})
    if content is not None:
        return content.get_text().strip()
    else:
        return ''


df_list = []

for i in range(len(base_info['dept'])):
    dept = base_info['dept'][i]
    dept_url = base_info['dept_url'][i]
    pages = base_info['pages'][i]
    for page in range(1, pages + 1):
        if page == 1:
            url = dept_url
        else:
            url = dept_url.replace('list.htm', 'list{}.htm'.format(page))

        html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
        bs0bj = BeautifulSoup(html, features='html.parser')
        #
        # print(bs0bj.prettify())
        # exit()
        infos = bs0bj.find('div', {'id': "wp_news_w3"}).find_all('a')
        names = [info.get_text().strip() for info in infos]
        urls = ["http://ee.gzu.edu.cn" + info.get('href') for info in infos]
        contents = [get_content(url) for url in urls]

        name_list = []
        title_list = []
        for name in names:
            name, title = name.split('【')
            name_list.append(name.replace(' ', '').strip())
            title_list.append(title.replace('】', '').strip())

        df = pd.DataFrame(
            {'姓名': name_list,
             'title': title_list,
             '信息': contents,
             'url': urls}
        )
        df['dept'] = dept

        df_list.append(df)

full_df = pd.concat(df_list)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
