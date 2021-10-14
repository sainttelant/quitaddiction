# -*- coding: utf-8 -*-

import requests
import json
import re
from bs4 import BeautifulSoup as bs
import os
import random
import time


class SignSpider(object):
    def __init__(self):
        print("init SignSpider!")
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.yuluju.com',

            'Cookie': 't=c675829116dca487cfd430cba9b715e9; r=1548; UM_distinctid=17c10b515c24a2-0f72a0a46a6f49-4343363-144000-17c10b515c3a9d; CNZZDATA1279885104=1915752153-1632363048-null%7C1632363048',
            'Referer': 'http://www.yuluju.com/lizhimingyan/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        self.url = "http://www.yuluju.com/lizhimingyan/"
        self.s = requests.Session()
        self.s.keep_alive = False
        self.path = os.getcwd()+"/wisdom"
        self.filename = self.path+"/wisdoms.txt"
        self.sentense = []
        self.day = 0

        # 当前日期
        self.time =  time.strftime('%Y-%m-%d', time.localtime(time.time()))

        self.summary = os.getcwd()+"/signsummary"
        self.summaryfile = self.summary+"/summary.txt"
        if not os.path.exists(self.summary):
            os.makedirs(self.summary)
        if not os.path.exists(os.getcwd() + "/wisdom"):
            os.makedirs(os.getcwd() + "/wisdom")
    
    def getlastline(self):
        """
        get last line of a file
        :param filename: file name
        :return: last line or None for empty file
        """
        try:
            filesize = os.path.getsize(self.summaryfile)
            if filesize == 0:
                return None
            else:
                with open(self.summaryfile, 'rb') as fp: # to use seek from end, must use mode 'rb'
                    offset = -8                 # initialize offset
                    while -offset < filesize:   # offset cannot exceed file size
                        fp.seek(offset, 2)      # read # offset chars from eof(represent by number '2')
                        lines = fp.readlines()  # read from fp to eof
                        if len(lines) >= 2:     # if contains at least 2 lines
                            return lines[-1]    # then last line is totally included
                        else:
                            offset *= 2         # enlarge offset
                    fp.seek(0)
                    lines = fp.readlines()
                    return lines[-1]
        except FileNotFoundError:
            print(self.summaryfile + ' not found!')
            return None


    def createsummary(self):
        infor = ""
        print("current time:",self.time)
        if not os.path.exists(self.summaryfile):
            with open(self.summaryfile,"a+") as file:
                file.write("you have been in a good habit for{}\tdays,date:{} !\n".format(self.day,self.time))
                infor = "you have been in a good habit for{}\tdays !\n".format(self.day)
        else:
            file = open(self.summaryfile,"a+")
            lines = self.getlastline()
            encoding = 'utf-8'
            # 从byte到str 转化
            line=lines.decode(encoding)
            numdays = line.split("days")[0].split("for")[1]
            
            historydate = line.split("date:")[1].split("!")[0]
            allhist = historydate.split("-")
            alltoday = self.time.split("-")
            c = False
            #判断 是否是同一天
            for a,b in zip(allhist,alltoday):
                if int(a)==int(b):
                    c = True
                else:
                    c = False
                    break
            if c:
                infor = "you have signed today, do not try to sign again, come tomorrow!"
            else:
                self.day=int(numdays)+1
                infor = "you have been in a good habit for{}\tdays,date:{} !\n".format(self.day,self.time)
                file.write(infor)
            file.close()
        return infor




    def Gethits(self):
        a = ""
        k = random.randint(0, 50)
        j = 0
        if not os.path.exists(self.filename):
            with open(self.path+"/wisdoms.txt", "a",encoding="utf-8") as f:
                print("begin to get hits!")
                ret = self.s.get(self.url, headers=self.headers)
                ret.encoding = ret.apparent_encoding
                if ret.status_code == 200:
                    print(ret.headers['content-type'])
                    msg = "get hits'channel successfull!"
                    soup = bs(ret.text, "html.parser")
                    for text in soup.select("ul li h2 a.title"):

                        href = "http://www.yuluju.com"+text['href']
                        newret = self.s.get(href, headers=self.headers)
                        newret.encoding = newret.apparent_encoding
                        if newret.status_code == 200:
                            print("access detail's web successfully")
                            soups = bs(newret.text, "lxml")
                            for infors in soups.select("div div span"):
                                j += 1
                                f.write(infors.get_text()+'\n')
                                if j==k:
                                    a = infors.get_text()
                else:
                    msg = "get hits'channel failure! check the internet request!"
                    #print(msg)
                    return msg
        else:
            print("gethits locally!")
            with open(self.filename, "r",encoding='UTF-8') as f:
                lines = f.readlines()
                for line in lines:
                    self.sentense.append(line)

            size_sentense = len(self.sentense)
            #print(self.sentense[random.randint(0, size_sentense)])
            a = self.sentense[random.randint(0, size_sentense)]

        return a


class Spiders(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                      ' (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.headers_m = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 '
                                        '(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

    # 形成富文本，参数是文本内容和字体颜色
    def getmsg(self, themsg, thecolor):
        msg = '<html><head/><body><p><span style=" font-family:Microsoft YaHei;font-size:9pt; color:{};">{}</span></p></body></html>'.format(
            thecolor, themsg)
        return msg

    # 从文件读取信息，返回一个列表
    def get_Infos(self, filename):
        Infos = []
        with open(filename, 'r') as f:
            data = f.readlines()
        for each in data:
            if len(each.strip()) > 0:
                Infos.append(each.strip())
        return Infos

    # 获取单个天猫商品DSR
    def get_TM(self, id, outfile):
        url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s' % id
        res = requests.get(url, headers=self.headers)
        html = res.text
        date = re.findall('json.*?\((.*)\)', html)[0]
        dsr = json.loads(date)['dsr']  # 转换成字典格式
        DSR = id + ',' + str(dsr['gradeAvg']).strip() + \
            ',' + str(dsr['rateTotal']).strip()
        with open(outfile, 'a') as f:
            f.write(DSR + '\n')
        return

    # 获取单个京东商品DSR
    def get_JD(self, id, outfile):
        url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=%s' % id
        res = requests.get(url, headers=self.headers)
        html = res.text
        dic = json.loads(html)['CommentsCount'][0]
        SkuId = str(dic['SkuId']).strip()  # 商品ID
        GoodRate = str(dic['GoodRate']).strip()  # 好评率
        GoodCount = str(dic['GoodCount']).strip()  # 好评数
        GeneralCount = str(dic['GeneralCount']).strip()  # 中评数
        PoorCount = str(dic['PoorCount']).strip()  # 差评数
        DSR = SkuId + ',' + GoodRate + ',' + GoodCount + \
            ',' + GeneralCount + ',' + PoorCount
        with open(outfile, 'a') as f:
            f.write(DSR + '\n')
        return

    # 获取天猫主图链接和价格
    def getimglink(self, ID, outfile):
        # 打开手机端网页
        url = "https://detail.m.tmall.com/item.htm?id={}".format(ID)
        html = requests.get(url, headers=self.headers_m).text
        try:
            soup = bs(html, "lxml")
            imglink = "https:" + \
                soup.select("div.itbox > a > img")[0].get("src")
        except:
            imglink = "miss"
        infos = re.findall('"price":"(\d+?\.\d\d)"', html)
        try:
            maxprice = max(list(map(float, infos)))
            minprice = min(list(map(float, infos)))
        except ValueError:
            maxprice = max(infos)
            minprice = min(infos)
        except:
            maxprice = "miss"
            minprice = "miss"
        thestr = ",".join([str(ID), imglink, str(maxprice), str(minprice)])
        with open(outfile, "a") as f:
            f.write(thestr + "\n")

    # 下载图片
    def downimg(self, savefile, savename, url):
        item = requests.get(url, headers=self.headers).content
        Imgname = savefile + '\\' + savename + '.jpg'
        with open(Imgname, 'wb') as f:
            f.write(item)
        return
