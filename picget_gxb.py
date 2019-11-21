# 国务院新闻办公室新闻发布会
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os,random,sys
from urllib.parse import urljoin
import re,uuid
# from op_oracle import *

# 本程序处理38114（不含）以后即2018年3月26日开始发布会
# 38114开始页面结构发生变化
# http://www.scio.gov.cn/xwfbh/xwbfbh/wqfbh/37601/38114/index.htm

filepath = r'C:\\360安全浏览器下载'
propath = os.getcwd()
kwlist = ['袭艳春']
index_list = ['http://www.scio.gov.cn/xwfbh/xwbfbh/index.htm']
flag = 1
download_flag = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
timeout=10
rstr = r"[\/\\\:\*\?\"\<\>\|]"
try:
    index_item = index_list[0]
    while flag == 1:
        r = requests.get(index_item, headers=headers, timeout=timeout)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        news_list = soup.find_all(href=re.compile('fbh/Document/'))
        np = soup.find('a', text='下一页')
        if np:
            index_item = urljoin(r.url, np.get('href'))
        else:
            flag = 0
        for news_item in news_list:
            count=0
            news_url = urljoin(index_item, news_item.get('href'))
            os.chdir(propath)
            driver = webdriver.Chrome()
            driver.get(news_url)
            # res = driver.find_element_by_link_text('图片直播')
            img_url = urljoin(news_url,driver.find_element_by_link_text('图片直播').get_attribute('href'))
            driver.close()
            r = requests.get(img_url, headers=headers, timeout=timeout)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "lxml")
            title = re.sub(rstr,"_",soup.find('title').text)
            div_list = soup.find_all('div', class_='bigcontent')
            for div_item in div_list:
                if kwlist[0] in div_item.text:
                    count = count + 1
                    os.chdir(filepath)
                    isExists = os.path.exists(kwlist[0])
                    if isExists:
                        print(kwlist[0], '文件夹已经存在了，不再创建')
                    else:
                        os.makedirs(kwlist[0])
                    os.chdir(kwlist[0])
                    if div_item.find("img") is None:
                        continue
                    img_r = requests.get(urljoin(img_url, div_item.find("img")["src"]),headers=headers, timeout=timeout)
                    print(img_r.status_code)
                    if img_r.status_code == 200:
                        pic_name = str(title) + str(count) + '.jpg'#str(random.randint(0, 10000))
                        for root, dirs, files in os.walk(os.getcwd()):
                            if pic_name in files:
                                download_flag = 1
                                print("已下载" + pic_name)
                                continue
                                # sys.exit(0)
                        if download_flag == 0 :
                            open(pic_name, 'wb').write(img_r.content)
                            print("Success" + re.sub(rstr,"_",div_item.text))
                    # print(div_item.text)
                pass
finally:
    pass

