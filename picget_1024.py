# xp1024.com 日本騎兵 最新合集
from bs4 import BeautifulSoup
#import urllib.request
import requests
import os
from urllib.parse import urljoin
import re,uuid
from op_oracle import *

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
# rooturl = 'http://1024.c2048ao.pw/'
rooturl = 'http://1024.c2048ao.pw/pw/'
avkeylist = ['LXV0','259LUXU','LXVS','prestige','古装']
clkeylist = ['最新合集']
# clkey1 = '日本騎兵'正片大片
urlkey = 'thread'
m = 1
n = 10
rtpath = os.getcwd()
r = requests.get(rooturl)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, "lxml")
atags = soup.find_all(['a'])
urllist = [urljoin(r.url, item.get('href')) \
        for item in atags \
         if item.get('href') \
         and urlkey in item.get('href') \
         and item.get('target') is None \
         and item.text in clkeylist \
         ]#and item.text == clkey1

def downlaodimg(url,m,n,key,rtpath):
    # 创建搜索关键字命名的目录    
    os.chdir(rtpath)
    isExists = os.path.exists(key)
    if isExists:
        print(key, '文件夹已经存在了，不再创建')
    else:
        os.makedirs(key)
    os.chdir(key)
    keypath = os.getcwd()
    # 逐页查找目标
    for x in range(n-m+1):
        # os.chdir(keypath)
        # 拼接完整的带页码目标网址
        crurl=url + "&page=" + str(m+x)
        r = requests.get(crurl)
        print(crurl)
        r.encoding='utf-8'        
        soup = BeautifulSoup(r.text, "lxml")
        temp1= soup.find_all('h3')
        # newpath = os.getcwd()
        for title in temp1:
            os.chdir(keypath)
            t = 1
            if title.find('a') is None:
                continue
            temp2= title.find('a')['href']
            urlt=urljoin(url, temp2)
            r = requests.get(urlt)
            soup = BeautifulSoup(r.text, "lxml")
            # 查找网页文本中是非存在所找关键字
            if key not in r.text:
                continue
            # 创建当前网页内容保存目录            
            print(urlt)
            rstr = r"[\/\\\:\*\?\"\<\>\|]"
            new_title = re.sub(rstr,"_",title.text)
            isExists = os.path.exists(new_title)
            if isExists:
                print(new_title, '文件夹已经存在了，不再创建')
                continue
            os.makedirs(new_title)
            os.chdir(new_title)
            print(new_title, '中有关键词！') # 连同网址urlt存入数据库
            wr_beauty(str(uuid.uuid1()),key,urlt,new_title)
            # 查找图片            
            ilist = soup.find_all('div',class_="tpc_content")
            for myimg in ilist:
                if myimg.find("img") is None:
                    continue
                temp3 = myimg.find_all("img")
                for temp4 in temp3:
                    temp5 = temp4["src"]        
                    ir = requests.get(temp5)
                    if ir.status_code == 200:
                        pic_name = str(t) + '.jpg'
                        open(pic_name, 'wb').write(ir.content)
                        print("Success!" + temp5)
                        t += 1     
for url in urllist:
    for key in avkeylist:
        downlaodimg(url,m,n,key,rtpath)
