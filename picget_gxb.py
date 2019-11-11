# 国务院新闻办公室新闻发布会
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os,random
from urllib.parse import urljoin
import re,uuid
# from op_oracle import *

# rooturl为首页地址，m为起始页，n为结束页
# key:keyword
# url='http://1024.c2048ao.pw/pw/thread.php?fid=83'
# url = 'https://www.wulinpai.com/18686.html'
# url = "http://1024.c2048ao.pw/pw/htm_data/3/1802/1021470.html"
# rooturl = 'http://s2.91sgc.rocks/pw/thread.php?fid=3'
# LXVS,39
# 259LUXU,71
# prestige,81
# LXV0,81

filepath = r'C:\\360安全浏览器下载'
propath = os.getcwd()
kwlist = ['袭艳春']
index_list = ['http://www.scio.gov.cn/xwfbh/xwbfbh/index.htm']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
rstr = r"[\/\\\:\*\?\"\<\>\|]"
try:
    for index_item in index_list:
        r = requests.get(index_item, headers=headers, timeout=3)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        news_list = soup.find_all(href=re.compile('fbh/Document/'))
        for news_item in news_list:
            news_url = urljoin(index_item, news_item.get('href'))
            os.chdir(propath)
            driver = webdriver.Chrome()
            driver.get(news_url)
            # res = driver.find_element_by_link_text('图片直播')
            img_url = urljoin(news_url,driver.find_element_by_link_text('图片直播').get_attribute('href'))
            driver.close()
            r = requests.get(img_url, headers=headers, timeout=3)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "lxml")
            title = re.sub(rstr,"_",soup.find('title').text)
            div_list = soup.find_all('div', class_='bigcontent')
            for div_item in div_list:
                if kwlist[0] in div_item.text:
                    os.chdir(filepath)
                    isExists = os.path.exists(kwlist[0])
                    if isExists:
                        print(kwlist[0], '文件夹已经存在了，不再创建')
                    else:
                        os.makedirs(kwlist[0])
                    os.chdir(kwlist[0])
                    if div_item.find("img") is None:
                        continue
                    img_r = requests.get(urljoin(img_url, div_item.find("img")["src"]),headers=headers, timeout=3)
                    print(img_r.status_code)
                    if img_r.status_code == 200:
                        pic_name = str(title) + str(random.randint(0, 10000)) + '.jpg'#
                        open(pic_name, 'wb').write(img_r.content)
                        print("Success!"+ div_item.text)
                    # print(div_item.text)
                pass
finally:
    pass

