import re

from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import pandas as pd

# base_url = "https://dzgc.xsyu.edu.cn/szdw/jsfc1/fjs1.htm"
# html = requests.get(base_url, headers={'User-Agent': UserAgent().random}).content
# bs0bj = BeautifulSoup(html, features='html.parser')
# print(bs0bj.contents)
#
# infos = bs0bj.find_all('script', {'language': "JavaScript"})
# print(infos)

names = ["郝小龙", "刘灿", "赵志峰", "毛艳慧", "吕方兴", "康正明", "胡长岭", "薛晓书", "田亚娟", "李周利", "崔占琴",
         "李长星", "肖志红", "薛朝妹", "刘升虎", "谢雁", "高理", "韦敏", "郭颖娜", "徐竟天", "陈延军", "唐俊", "闫宏亮",
         "刘光星", "苏娟", "景明利", "朱冰", "解茜草", "高怡", "吴银川", "宋久旭", "任志平", "张妙瑜", "赵晓姣",
         "刘彦萍", "燕并男", "谢海明", "杨一", "甘伟", "樊恒", "高建申", "郝小龙", "王小鑫", "饶丽婷"]
ids = ["3417", "3416", "3415", "3414", "3413", "3412", "2704", "2703", "2702", "2699", "2701", "2700", "2697", "2696",
       "2694", "2695", "3155", "2693", "2692", "2691", "3162", "2689", "2686", "2687", "2688", "2681", "2682", "2678",
       "2679", "2680", "2675", "2672", "2673", "3154", "3151", "2671", "3163", "3161", "2670", "3153", "3159", "3152",
       "3156", "3158"]

urls = [
    "https://dzgc.xsyu.edu.cn/info/1212/{}.htm".format(i) for i in ids
]


def get_info(url):
    html = requests.get(url, headers={'User-Agent': UserAgent().random}).content
    bs0bj = BeautifulSoup(html, features='html.parser')
    infos = bs0bj.find('div', {'class': "v_news_content"})
    return infos.get_text().strip()


info_list = [
    get_info(url) for url in urls
]

full_df = pd.DataFrame(
    {'姓名': names,
     'url': urls,
     '信息': info_list}
)

full_df.to_csv('teacher_info.csv', index=False, encoding='utf-8-sig')
