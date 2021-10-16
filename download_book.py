import requests
import re
import os
import docx
import pyinputplus as pyip
from pathlib import Path

class DownloadBooks:
    """下载小说"""

    def __init__(self,netPlace,book_text="",book_number=""):
        """初始化数据"""
        self.netPlace = netPlace
        if book_text:
            self.book_text = book_text
        else:
            raise Exception("No book text")
        if book_number:
            self.book_number = book_number
        else:
            raise Exception("No book number")

    def book_res(self):
        """网页代码"""
        self.res = requests.get(self.netPlace)

    def res_filename(self):
        """文件名称"""
        file_net = (self.netPlace.replace("/","_")).replace(":","")
        p = Path("E:/Books")/f"{self.book_text}"/f"{self.book_text}{book_number}"
        if not p.exists():
            os.makedirs(p)
        self.resFilename = p/f"{self.book_text}{book_number}.txt"

    def _res_file(self,mode,ecding="",filename=""):
        """打开文件"""
        if filename:
            if ecding:
                self.resFile = open(filename,mode,encoding=ecding)
            else:
                self.resFile = open(filename,mode)
        else:
            if ecding:
                self.resFile = open(self.resFilename,mode,encoding=ecding)
            else:
                self.resFile = open(self.resFilename,mode)

    def write_b_res(self):
        """写入源码"""
        self._res_file("wb")
        for bites in self.res.iter_content(1000000):
            self.resFile.write(bites)
        self.resFile.close()

    def read_res(self):
        """读取文件"""
        self._res_file("r","utf-8")
        self.res_content = self.resFile.read()
        self.resFile.close()

    def regex_res(self):
        """寻找文本"""
        res_re_bookname = re.compile(r'<h1>(.*?)</h1>')
        self.res_content_bookname = res_re_bookname.findall(self.res_contents)[0]
        res_re_text = re.compile(r'<div id="content">(.*?)</div>',re.DOTALL)
        self.res_content_text = res_re_text.findall(self.res_contents)[0]

    def res_text(self):
        """整理格式"""
        self.res_text = ((self.res_content_text.replace("<br />","")
                         ).replace("&nbsp"," ")).replace("/n/n","/n")

    def write_res_text(self):
        """写入文本"""
        self._res_file("w","utf-8")
        self.resFile.write(self.res_content_bookname)
        self.resFile.write(self.res_text)
        self.resFile.close()

    def docx_wirte(self):
        """导入docx文档"""
        os.chdir(p)
        doc = docx.Ducument()
        doc.add_heading(self.res_content_bookname,0)
        doc.add_paragraph(self.res_text)
        doc.save(f"{self.book_text}{book_number}.docx"

    def all_db(self):
        self.book_res()
        self.res_filename()
        self.write_b_res()
        self.read_res()
        self.regex_res()
        self.res_text()
        self.write_res_text()
        self.docx_write()


def bookNumber(num):
    if num >= 100000:
        return f"第{num}章"
    elif num >= 10000:
        return f"第0{num}章"
    elif num >= 1000:
        return f"第00{num}章"
    elif num >= 100:
        return f"第000{num}章"
    elif num >= 10:
        return f"第0000{num}章"
    elif num >= 1:
        return f"第00000{num}章"
    else:
        return None

def main():
    net_name = input("请输入网站域名:\n")
    start_num = pyip.inputInt(promrt="请输入起始数字:\n")
    end_num = pyip.inputInt(promrt="请输入结束数字:\n")
    book_name = input("请输入书本名称:\n")

    for net_num in range(start_num,end_num+1):
        book_num = bookNumber(net_num-start_num+1)
        db = DownloadBooks(f"{net_name}/{net_num}.html",book_name,book_num)
        db.all_db()
        print(f"已下载{book_num}")

    print("Done.")

if __name__ == "__main__":
    main()
