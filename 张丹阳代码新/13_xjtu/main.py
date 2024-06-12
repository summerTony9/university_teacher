import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_info = {
    'dept': ["光学检测技术研究所", "生物检测与仪器研究所", "智能传感与系统研究所", "智能检测技术与系统研究所",
             "学科交叉-X中心"],
    'dept_url': [
        "https://ist.xjtu.edu.cn/szdw/jsml1/gxjcjsyjs.htm",
        "https://ist.xjtu.edu.cn/szdw/jsml1/swjcyyqyjs.htm",
        "https://ist.xjtu.edu.cn/szdw/jsml1/zncgyxtyjs.htm",
        "https://ist.xjtu.edu.cn/szdw/jsml1/znjcjsyxtyjs.htm",
        "https://ist.xjtu.edu.cn/szdw/jsml1/xkjc_Xzx.htm",
        # "http://cetong.hrbust.edu.cn/gdxxkxygc/list.htm",
        # "http://cetong.hrbust.edu.cn/cslm/list.htm",
        # "http://cetong.hrbust.edu.cn/748/list.htm",
    ],
    'pages': [1, 2, 3, 1, 1]
}


def get_info(url):
    # url = "http://cetong.hrbust.edu.cn/744/list.htm"
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    #
    # print(bs0bj.prettify())
    # exit()
    infos = bs0bj.find_all('li', {"data-aos": "fade-up"})
    names = [info.find('h3').get_text().strip() for info in infos]
    names = [name.replace(" ", '') for name in names]
    urls = ["https://ist.xjtu.edu.cn/" + re.search(r'info.*', info.find('a').get('href')).group() for info in infos]

    return pd.DataFrame(
        {'姓名': names,
         'url': urls}
    )

df_list = []

for i in range(len(base_info['dept'])):
    title = base_info['dept'][i]
    dept_url = base_info['dept_url'][i]
    pages = base_info['pages'][i]
    for page in range(1, pages + 1):
        if page == 1:
            url = dept_url
        else:
            url = dept_url.replace('.htm', '/{}.htm'.format(page-1))
            print(url)
        df = get_info(url)
        df['dept'] = title
        df_list.append(df)

full_df = pd.concat(df_list)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')

