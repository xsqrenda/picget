# 国务院政策例行吹风会（国务院新闻办公室主持）
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os,random,sys
from urllib.parse import urljoin
import re,uuid
# from op_oracle import *

# http://www.scio.gov.cn/xwfbh/xwbfbh/wqfbh/37601/38114/index.htm
# 根据2020-06-15发布的《山东省人民政府关于任免袭艳春等工作人员职务的通知》
# http://www.shandong.gov.cn/art/2020/6/15/art_107851_107498.html
# 袭艳春为山东省人民政府新闻办公室主任。故该程序暂停。

filepath = os.getcwd()
propath = os.getcwd()
kwlist = ['袭艳春']
index_list = ['http://sousuo.gov.cn/column/31510/0.htm']
# 正式的地址为：国务院政策吹风会_新闻发布_中国政府网  http://www.gov.cn/xinwen/fabu/zccfh/index.htm
flag = 1
download_flag = 0
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
timeout=100
rstr = r"[\/\\\:\*\?\"\<\>\|]"
try:
    index_item = index_list[0]
    while flag == 1:
        r = requests.get(index_item, headers=headers, timeout=timeout)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "lxml")
        news_list = soup.find_all(href=re.compile('zccfh'))
        np = soup.find('a', text='下一页')
        if np:
            index_item = urljoin(r.url, np.get('href'))
        else:
            flag = 0
        for news_item in news_list:
            count=0
            news_url = news_item.get('href')
            os.chdir(propath)
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # driver = webdriver.Chrome(chrome_options=chrome_options)
            # driver.get(news_url)
            # nexturl = driver.find_element_by_link_text('图片直播')
            r = requests.get(news_url, headers=headers, timeout=timeout)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "lxml")
            title = re.sub(rstr, "_", soup.find('title').text)
            temp_list1 = soup.find_all(href=re.compile('xctp.htm'))
            next_url_1 = urljoin(news_url,temp_list1[0].get('href'))
            r = requests.get(next_url_1, headers=headers, timeout=timeout)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "lxml")
            div_list = soup.find_all('div', class_='tplgd_wz')
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
                    next_url_2 = urljoin(news_url,div_item.find('a').get('href'))
                    r = requests.get(next_url_2, headers=headers, timeout=timeout)
                    r.encoding = 'utf-8'
                    soup = BeautifulSoup(r.text, "lxml")
                    img_list = soup.find_all('div', class_='pages_content')
                    if img_list[0].find("img") is None:
                        continue
                    img_r = requests.get(urljoin(next_url_2, img_list[0].find("img")["src"]),headers=headers, timeout=timeout)
                    print(img_r.status_code)
                    if img_r.status_code == 200:
                        pic_name = str(title) + str(count) + '.jpg'#str(random.randint(0, 10000))
                        for root, dirs, files in os.walk(os.getcwd()):
                            if pic_name in files:
                                download_flag = 1
                                print("已下载" + pic_name)
                                flag = 0
                                continue
                                # sys.exit(0)
                        if download_flag == 0 :
                            open(pic_name, 'wb').write(img_r.content)
                            print("Success" + re.sub(rstr,"_",div_item.text))
                    # print(div_item.text)
                pass
finally:
    pass

