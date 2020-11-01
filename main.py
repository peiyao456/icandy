# -*- coding:utf-8 -*-
import  http.cookiejar
from urllib import request
import requests
from bs4 import BeautifulSoup

url = "https://movie.douban.com/top250"
# response1 = request.urlopen(url,timeout=10)
# print("第一种方法")
# # 获取状态码，200表示成功
# print(response1.getcode())
# # 获取网页内容的长度
# print(response1.read())
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
# r = requests.get(url,headers=headers)
# print(type(r.text))
# print(r.status_code)
# ret = request.Request(url, headers=headers)
# res = request.urlopen(ret)
# aa = res.read().decode('utf-8')
# soup0 = BeautifulSoup(aa)
# print(soup0)


def get_all_text():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    for i in range(10):
        url = "https://movie.douban.com/top250?start="+str(i*25)+"&filter="
        ret = request.Request(url, headers=headers)  # 创建request请求对象
        res = request.urlopen(ret)
        aa = res.read().decode('utf-8')  # 得到页面 读取内容
        soup0 = BeautifulSoup(aa)  # html文件解析器
        li = soup0.find_all('div',class_='item')
        print("li=",li)
        for x in li:
            id = x.find('div',class_='pic').find('em').text
            title = x.find('div',class_='hd').find('a').find('span').text
            pf = x.find('div',class_='star').find('span',class_='rating_num').text
            src_p = x.find("div",class_='pic').find('img')['src']
            print("id={},title={},pf={},src={}".format(id,title,pf,src_p))
            # ret_pic = request.Request(src_p,headers=headers)
            # f = open("p.jpg",'w')
            # buf = request.urlopen(src_p).read()
            # f.write(buf)
            # pass

get_all_text()
