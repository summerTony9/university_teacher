from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

base_url = "https://oeis.dlut.edu.cn/szdw/jslb.htm"
html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
bs0bj = BeautifulSoup(html, features='html.parser')

infos = bs0bj.find_all('div', {'class': 'jswo'})
names = []
titles = []
gras = []
degrees = []
universities = []

for info in infos:
    info_text = info.get_text()
    info_split = info_text.split("\n")
    info_split = [i for i in info_split if i != '' and i != ' ']
    names.append(info_split[0].split("：")[1])
    titles.append(info_split[1].split("：")[1])
    gras.append(info_split[2].split("：")[1])
    degrees.append(info_split[3].split("：")[1])
    universities.append(info_split[4].split("：")[1])

full_df = pd.DataFrame(
    {'姓名': names,
     '职称': titles,
     '学历': gras,
     '学位': degrees,
     '毕业院校': universities}
)
full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')

