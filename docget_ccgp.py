# 国务院新闻办公室新闻发布会
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os,random,sys,pytesseract
from img_process import *
from PIL import Image
from urllib.parse import urljoin
import re,uuid
# from op_oracle import *

# 本程序处理38114（不含）以后即2018年3月26日开始发布会
# 38114开始页面结构发生变化
# http://www.scio.gov.cn/xwfbh/xwbfbh/wqfbh/37601/38114/index.htm




filepath = r'C:\\360安全浏览器下载'
propath = os.getcwd()
kwlist = ['袭艳春']
index_list = ['http://htgs.ccgp.gov.cn/GS8/contractpublish/search']
flag = 1
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
rstr = r"[\/\\\:\*\?\"\<\>\|]"
yzm_fn = 'yzm.jpg'
yzmhd_fn = 'yzm1.jpg'
yzmez_fn = 'yzm2.jpg'
yzmqz_fn = 'yzm3.jpg'
yzmcj_fn = 'yzm3.jpg'
gys_name = '中电万维'
pytesseract.pytesseract.tesseract_cmd='D:\program\Tesseract-OCR\\tesseract.exe'
try:
    index_item = index_list[0]
    while flag == 1:
        # r = requests.get(index_item, headers=headers, timeout=3)
        # # r.raise_for_status()
        # if r.status_code == 200:
        #     r.encoding = 'utf-8'
        #     soup = BeautifulSoup(r.text, "lxml")
        #     yzm = soup.find('div', id="codeImgDiv").find('src')
        driver = webdriver.Chrome()
        driver.get(index_item)
        url_src = driver.find_element_by_xpath('//*[@id="codeImgDiv"]/img').get_attribute('src')
        if url_src:
            img_r = requests.get(url_src, headers=headers, timeout=3)
            print(img_r.status_code)
            if img_r.status_code == 200:
                # str(random.randint(0, 10000))
                open(yzm_fn, 'wb').write(img_r.content)
                print("成功下载验证码图片。")
                image = Image.open(yzm_fn)
                yzmhd = image.convert("L")
                yzmez = binarizing(yzmhd,140)
                yzmqz = de_point(yzmez)
                yzmcj = yzmqz.crop((0, 0, 100, 32))
                yzmst = pytesseract.image_to_string(yzmcj, lang='eng', config='--psm 6')
                print(yzmst)
                driver.find_element_by_name('code').send_keys(yzmst)
                driver.find_element_by_name('searchSupplyName').send_keys(gys_name)
                driver.find_element_by_id('queryBtn').click()
                flag = 0

        # from PIL import Image
        # from img_process import *
        #
        # image = Image.open('yzm1.jpg')
        # img1 = image.convert("L")
        # img1.save('img1.jpg')
        # img2 = binarizing(img1, 140)
        # img2.save('img2.jpg')
        # img3 = de_point(img2)
        # img3.save('img3.jpg')
        # import tesserocr
        # img4 = img3.crop(((0, 0, 100, 30)))
        # img4.save('img4.jpg')
        # result = tesserocr.image_to_text(img4)
        # result
        # ''
        # img4 = img3.crop(((0, 0, 100, 32)))
        # img4.save('img4.jpg')
        # result = tesserocr.image_to_text(img4)
        # result


        # np = soup.find('a', text='下一页')
        # if np:
        #     index_item = urljoin(r.url, np.get('href'))
        # else:
        #     flag = 0
        # for news_item in news_list:
        #     count=0
        #     news_url = urljoin(index_item, news_item.get('href'))
        #     os.chdir(propath)
        #     driver = webdriver.Chrome()
        #     driver.get(news_url)
        #     # res = driver.find_element_by_link_text('图片直播')
        #     img_url = urljoin(news_url,driver.find_element_by_link_text('图片直播').get_attribute('href'))
        #     driver.close()
        #     r = requests.get(img_url, headers=headers, timeout=3)
        #     r.encoding = 'utf-8'
        #     soup = BeautifulSoup(r.text, "lxml")
        #     title = re.sub(rstr,"_",soup.find('title').text)
        #     div_list = soup.find_all('div', class_='bigcontent')
        #     for div_item in div_list:
        #         if kwlist[0] in div_item.text:
        #             count = count + 1
        #             os.chdir(filepath)
        #             isExists = os.path.exists(kwlist[0])
        #             if isExists:
        #                 print(kwlist[0], '文件夹已经存在了，不再创建')
        #             else:
        #                 os.makedirs(kwlist[0])
        #             os.chdir(kwlist[0])
        #             if div_item.find("img") is None:
        #                 continue
        #             img_r = requests.get(urljoin(img_url, div_item.find("img")["src"]),headers=headers, timeout=3)
        #             print(img_r.status_code)
        #             if img_r.status_code == 200:
        #                 pic_name = str(title) + str(count) + '.jpg'#str(random.randint(0, 10000))
        #                 for root, dirs, files in os.walk(os.getcwd()):
        #                     if pic_name in files:
        #                         print("已下载" + pic_name)
        #                         continue
        #                         # sys.exit(0)
        #                 open(pic_name, 'wb').write(img_r.content)
        #                 print("Success!" + div_item.text)
        #             # print(div_item.text)
        #         pass
finally:
    pass

