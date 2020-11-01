# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import os
import shutil
import sqlite3


class Spider(object):
    """
    爬虫类
    """
    base_url = "https://movie.douban.com/top250?start="
    save_info_path = "豆瓣电影top250.xls"
    pic_path = "./pic"
    db_path = "movie.db"

    def main(self):
        # 获取数据
        data_list = self.getData()
        # 保存数据
        self.saveData(data_list)
        self.savePic(data_list)

    def getData(self):
        print("开始获取数据...")
        dataList = []
        find_link = re.compile(r'<a href="(.*?)">')
        find_imgsrc = re.compile(r'<img.*src="(.*?)"',re.S)
        find_title = re.compile(r'<span class="title">(.*)</span>')
        find_rating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
        find_judge = re.compile(r'<span>(\d*)人评价</span>')
        find_bd = re.compile(r'<p class="">(.*?)</p>',re.S)
        find_inq = re.compile(r'<span class="inq">(.*?)</span>', re.S)
        for i in range(0,10):
            url = self.base_url+str(i*25)
            html = self.askUrl(url)
            # 数据解析
            soup = BeautifulSoup(html,"html.parser")
            for item in soup.find_all("div",class_="item"):
                data = []
                item = str(item)
                link = re.findall(find_link,item)[0]
                data.append(link)
                imgsrc = re.findall(find_imgsrc,item)[0]
                data.append(imgsrc)
                titles = re.findall(find_title,item)
                data.append(titles[0])
                if len(titles) == 2:
                    data.append(titles[1].replace("/",""))
                else:
                    data.append('')  # 英文标题留空
                rating = re.findall(find_rating,item)[0]
                data.append(rating)
                judge = re.findall(find_judge,item)[0]
                data.append(judge)
                inq = re.findall(find_inq,item)
                if len(inq) > 0:
                    inq = inq[0].replace("。","")
                else:
                    inq = " "
                data.append(inq)
                bd = re.findall(find_bd,item)[0]
                bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)

                bd = re.sub("/","",bd)
                data.append(bd.strip())
                # print(bd.strip())

                dataList.append(data)

        return dataList

    def askUrl(self,url):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        req = urllib.request.Request(url=url,headers=headers)
        try:
            respose = urllib.request.urlopen(req, timeout=3)
            html = respose.read().decode("utf-8")
        except urllib.error.URLError as e:
            if hasattr(e,"code"):
                print("失败码：",e.code)
            if hasattr(e,"reason"):
                print("失败原因：",e.reason)
        return html

    def saveData(self, data_list):
        print("开始保存数据到Excel...")
        book = xlwt.Workbook(encoding="utf-8")
        sheet = book.add_sheet("豆瓣电影top250",cell_overwrite_ok=True)
        col = ("NO.","链接","图片链接","影片中文名","影片外文名","评分","评价数","概况","相关信息")
        for i in range(len(col)):
            sheet.write(0,i,col[i])
        for i in range(0,len(data_list)):
            # print("第%d条" % (i+1))
            data = data_list[i]
            sheet.write(i+1,0,i+1)  # 把序号写到excel中
            for j in range(1,len(col)):
                sheet.write(i+1,j,data[j-1])
        book.save(self.save_info_path)

    def savePic(self, data_list):
        """
        保存电影海报到本地
        :param dataList:
        :return:
        """
        print("开始保存电影海报到本地...")
        if not os.path.exists(self.pic_path):  # 不存在就创建
            os.makedirs(self.pic_path)
        if len(os.listdir(self.pic_path)) > 0:
            # 清空
            shutil.rmtree(self.pic_path)
            os.makedirs(self.pic_path)

        for i in range(len(data_list)):
            pic_url = data_list[i][1]
            title = data_list[i][2]
            urllib.request.urlretrieve(pic_url,"{}/{}_{}.jpg".format(self.pic_path,i+1,title))

        return

    def saveDB(self,data_list):
        pass

    def createDB(self):
        sql = '''
        create table movie256 
        (
        id integer primark key autocrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        introduction text,
        info text
        )
        '''
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()


if __name__ == "__main__":
    s = Spider()
    s.createDB()