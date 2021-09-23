# -*- coding: utf-8 -*-

import datetime
import os.path
import sys
import time

import cv2
from PyQt5 import QtCore, QtWidgets

from APIs import SignSpider, Spiders
from ToolUI import Ui_MainWindow


class MainUI(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.aboutmsg = "version1.0\n\n The aim of this software is to help people to quit addictions" \
                        "Fuction 1、Sign in everyday,and Record your apprearance varying \n\n" \
                        "Fuction 2、Daily hits or Wisdom words \n\n " \
                        "Fuction 3、Punishment mechanism, violate rules will randomly delete one of \n\n" \
                        "your favourable videos, where you specified folder path \n\n" \
                        "Date：2021-9-8\n"
        self.authormsg = "Author:wilson\n" \
                         "Contact me\nQQ：525324158\n"

        self.actionOpenfile.triggered.connect(
            QtWidgets.QFileDialog.getOpenFileName)  # 查看当前文件夹
        self.actionQiut.triggered.connect(self.close)  # 菜单栏退出按钮函数
        self.actionAbout.triggered.connect(
            lambda: self.selectInfo("About", self.aboutmsg))  # 关于软件
        self.actionAuthor.triggered.connect(
            lambda: self.selectInfo("Author", self.authormsg))  # 关于作者
        self.pushButton_3.clicked.connect(self.startdsr)  # DSR开始按钮
        #self.pushButton_4.clicked.connect(self.startlink)  # 主图开始按钮

        # capture button click
        # self.pushButton_5.clicked.connect(self.startimg)  # 批量下载图片开始按钮
        self.pushButton_5.clicked.connect(self.capture)
        # 签到是pushbotton4 ， 显示是 text4
        self.pushButton_4.clicked.connect(self.sign)

    # 重写关闭函数

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Close',
                                               "Close will terminate the downloading process,verify\nClose？",
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 消息框函数，传入2个参数，第1个是标题，第2个是显示内容
    def selectInfo(self, thetitle, megs):
        QtWidgets.QMessageBox.about(self, thetitle, megs)

    # 提取DSR中商品类型
    def changePD(self):
        if self.radioButton_1.isChecked():
            product = "tmall"
        if self.radioButton_2.isChecked():
            product = "jingdong"
        return product

    # 更新状态栏
    def statusshow(self, astr):
        self.statusbar.showMessage(astr)

    # DSR槽函数---------------------------------------------------------------------------------------------------
    # 启动DSR线程的槽函数
    def startdsr(self):
        self.statusbar.setStyleSheet("color:green")
        self.pushButton_5.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_3.setText("")  # 插入一个空白，每次启动线程都可以清屏
        txtname = self.lineEdit_34.text()
        """
        product = self.changePD()
        self.dsrthread = dsrThread(txtname, product)
        self.dsrthread.status_signal.connect(self.statusshow)
        self.dsrthread.dsrtext_signal.connect(self.dsrtextshow)
        self.dsrthread.dsrprogmax_signal.connect(self.dsrprog_max)
        self.dsrthread.dsrprog_signal.connect(self.dsrprog_value)
        self.dsrthread.finished.connect(self.dsrpushon)  # 线程结束执行函数
        self.dsrthread.start()
        """
    # 线程结束后开启DSR按钮

    def dsrpushon(self):
        self.pushButton_1.setDisabled(False)

    # 更新DSR输出文本
    def dsrtextshow(self, astr):
        self.textEdit_1.append(astr)

    # 获取DSR进度条最大值
    def dsrprog_max(self, n):
        self.progressBar_1.setMinimum(0)
        self.progressBar_1.setMaximum(n)

    # 更新DSR进度条
    def dsrprog_value(self, i):
        self.progressBar_1.setValue(i)

    # 主图链接槽函数------------------------------------------------------------------------------------------------
    def startlink(self):
        self.statusbar.setStyleSheet("color:blue")
        self.pushButton_3.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_4.setText("")  # 插入一个空白，每次启动线程都可以清屏
        txtname = self.lineEdit_34.text()
        self.linkthread = linkThread(txtname)
        self.linkthread.status_signal.connect(self.statusshow)
        self.linkthread.linktext_signal.connect(self.linktextshow)
        self.linkthread.progmax_signal.connect(self.linkprog_max)
        self.linkthread.progvalue_signal.connect(self.linkprog_value)
        self.linkthread.finished.connect(self.linkpushon)  # 线程结束执行函数
        self.linkthread.start()

    def linkpushon(self):
        self.pushButton_3.setDisabled(False)

    def linktextshow(self, astr):
        self.textEdit_4.append(astr)

    def linkprog_max(self, n):
        self.progressBar_4.setMinimum(0)
        self.progressBar_4.setMaximum(n)

    def linkprog_value(self, i):
        self.progressBar_2.setValue(i)

    # 批量下载图片槽函数----------------------------------------------------------------------------------------------
    def startimg(self):
        self.statusbar.setStyleSheet("color:green")
        self.pushButton_5.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_3.setText("")  # 插入一个空白，每次启动线程都可以清屏
        txtname = self.lineEdit_31.text()
        imgfile = self.lineEdit_32.text()
        self.imgthread = imgThread(txtname, imgfile)
        self.imgthread.status_signal.connect(self.statusshow)
        self.imgthread.imgtext_signal.connect(self.imgtextshow)
        self.imgthread.progmax_signal.connect(self.imgprog_max)
        self.imgthread.progvalue_signal.connect(self.imgprog_value)
        self.imgthread.finished.connect(self.imgpushon)  # 线程结束执行函数
        self.imgthread.start()

    def capture(self):
        print("capture your face")
        self.pushButton_5.setDisabled(True)  # 线程启动锁定按钮
        self.textEdit_5.setText("")  # 插入一个空白，每次启动线程都可以清屏
        folderpath = self.lineEdit_36.text()
        self.capthread = capThread(folderpath)
        self.capthread.captext_signal.connect(self.imgtextshow)
        self.capthread.finished.connect(self.imgpushon)
        self.capthread.start()

    def sign(self):
        print("begin to sign everyday")
        self.pushButton_4.setDisabled(True)
        self.textEdit_4.setText("")
        self.sign = sign()
        self.sign.signtext_signal.connect(self.signtextshow)
        self.sign.finished.connect(self.signpushon)
        self.sign.start()
    

    def imgpushon(self):
        self.pushButton_5.setDisabled(False)

    def signpushon(self):
        self.pushButton_4.setDisabled(False)

    def imgtextshow(self, astr):
        self.textEdit_5.append(astr)

    def signtextshow(self,astr):
        self.textEdit_4.append(astr)

    def imgprog_max(self, n):
        self.progressBar_3.setMinimum(0)
        self.progressBar_3.setMaximum(n)

    def imgprog_value(self, i):
        self.progressBar_3.setValue(i)


# DSR线程
class dsrThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)  # 发送给状态栏的信号
    dsrtext_signal = QtCore.pyqtSignal(str)  # 发送给DSR输出框的信号
    dsrprogmax_signal = QtCore.pyqtSignal(int)  # 发送给进度条的信号，给出最大值
    dsrprog_signal = QtCore.pyqtSignal(int)  # 发送给进度条的信号，给出每次刷新的进度

    def __init__(self, txtname, product):  # 参数：读取的文件名，商品类型
        super().__init__()
        self.txtname = txtname
        self.product = product
        self.api = Spiders()

    def run(self):
        start = time.time()
        T = datetime.datetime.now()
        self.status_signal.emit("当前状态：正在进行DSR提取操作...")
        try:
            IDs = self.api.get_Infos(self.txtname)
        except:
            self.dsrtext_signal.emit(
                self.api.getmsg("读取文件失败，请检查文件名称是否有误！", "red"))
        else:
            nums = len(IDs)
            self.dsrprogmax_signal.emit(nums)
            i = 1
            if self.product == "tmall":
                outfile = "TMdsr_" + \
                    T.strftime("%Y%m%d%H%M") + "_" + str(nums) + ".csv"
                self.dsrtext_signal.emit(self.api.getmsg(
                    "商品类型为【天猫商品】，有效ID总计{}个，开始提取DSR".format(nums), "#464749"))
                with open(outfile, 'w') as f:
                    f.write('商品ID,评分,评论数\n')
                for each in IDs:
                    try:
                        self.api.get_TM(each, outfile)
                    except:
                        msg_b = "总计{}个商品ID,第{}个商品：{}写入信息失败！".format(
                            nums, i, each)
                        self.dsrtext_signal.emit(self.api.getmsg(msg_b, "red"))
                    else:
                        msg_c = "总计{}个商品ID,成功写入第{}个天猫商品：{}".format(
                            nums, i, each)
                        self.dsrtext_signal.emit(
                            self.api.getmsg(msg_c, "#464749"))
                        self.dsrprog_signal.emit(i)
                    i += 1
            elif self.product == "jingdong":
                outfile = "JDdsr_" + \
                    T.strftime("%Y%m%d%H%M") + "_" + str(nums) + ".csv"
                self.dsrtext_signal.emit(self.api.getmsg(
                    "商品类型为【京东商品】，有效ID总计{}个，开始提取DSR".format(nums), "#464749"))
                with open(outfile, 'w') as f:
                    f.write('SKUID,好评率,好评数,中评数,差评数\n')
                for each in IDs:
                    try:
                        self.api.get_JD(each, outfile)
                    except:
                        msg_b = "总计{}个商品ID,第{}个商品：{}写入信息失败！".format(
                            nums, i, each)
                        self.dsrtext_signal.emit(self.api.getmsg(msg_b, "red"))
                    else:
                        msg_c = "总计{}个商品ID,成功写入第{}个京东商品：{}".format(
                            nums, i, each)
                        self.dsrtext_signal.emit(
                            self.api.getmsg(msg_c, "#464749"))
                        self.dsrprog_signal.emit(i)
                    i += 1
            end = time.time()
            msg_d = "DSR提取完毕，耗时：%0.2f秒！\n数据保存在当前目录下表格  %s  中" % (
                float(end - start), outfile)
            self.dsrtext_signal.emit(self.api.getmsg(msg_d, "green"))
        self.status_signal.emit("当前状态：DSR信息提取操作完毕！")


class linkThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)
    linktext_signal = QtCore.pyqtSignal(str)
    progmax_signal = QtCore.pyqtSignal(int)
    progvalue_signal = QtCore.pyqtSignal(int)

    def __init__(self, txtname):
        super().__init__()
        self.txtname = txtname
        self.api = Spiders()

    def run(self):
        start = time.time()
        T = datetime.datetime.now()
        self.status_signal.emit("当前状态：正在进行天猫主图链接提取操作...")
        try:
            IDs = self.api.get_Infos(self.txtname)
        except:
            self.linktext_signal.emit(
                self.api.getmsg("读取文件失败，请检查文件名称是否有误！", "red"))
        else:
            nums = len(IDs)
            outfile = "links_" + \
                T.strftime("%Y%m%d%H%M") + "_" + str(nums) + ".csv"
            with open(outfile, "w") as f:
                f.write("商品ID,主图链接,原价,折扣价" + "\n")
            self.progmax_signal.emit(nums)
            self.linktext_signal.emit(self.api.getmsg(
                "读取文件成功，有效ID总计{}个，开始提取天猫主图链接".format(nums), "#464749"))
            i = 1
            for each in IDs:
                try:
                    self.api.getimglink(each, outfile)
                except:
                    msg_b = "总计{}个商品ID,第{}个商品：{}写入信息失败！".format(nums, i, each)
                    self.linktext_signal.emit(self.api.getmsg(msg_b, "red"))
                else:
                    msg_c = "总计{}个商品ID,成功写入第{}个天猫主图信息：{}".format(nums, i, each)
                    self.linktext_signal.emit(
                        self.api.getmsg(msg_c, "#464749"))
                    self.progvalue_signal.emit(i)
                    
                i += 1
            end = time.time()
            msg_d = "天猫主图链接提取完毕，耗时：%0.2f秒！\n数据保存在当前目录下表格  %s  中" % (
                float(end - start), outfile)
            self.linktext_signal.emit(self.api.getmsg(msg_d, "green"))
        self.status_signal.emit("当前状态：天猫主图信息提取操作完毕！")

class sign(QtCore.QThread):
    sign_signal  =QtCore.pyqtSignal(str)
    signtext_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.api = SignSpider()

    def run(self):
        self.signtext_signal.emit("click sign if you keep good habits!!")
        text = self.api.Gethits()
        self.signtext_signal.emit(text)

    



class capThread(QtCore.QThread):
    capture_signal = QtCore.pyqtSignal(str)
    captext_signal = QtCore.pyqtSignal(str)

    def __init__(self, folders):
        super().__init__()
        self.folders = folders

    def run(self):
        start = time.time()
        self.captext_signal.emit(
            "you are now recording your progress everyday")
        if not os.path.exists(self.folders):
            self.captext_signal.emit(
                "create a %s folder to record your progress" % (self.folders))
            os.mkdir(self.folders)
        else:
            print("current path:", os.getcwd())
            print("folders:", self.folders)
            savepath = os.path.join(os.getcwd(), self.folders)
            print(savepath)
            cap = cv2.VideoCapture(0)
            currtime = time.strftime(
                '%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            print(currtime)
            picname = savepath+"/"+currtime+"_face.jpg"
            print(picname)
            count = 5
            while(True):
                # get a frame
                ret, frame = cap.read()
                # show a frame, 无法imshow，出错
                self.captext_signal.emit("begin to count down %d !"%(count))
                time.sleep(1)
                count-=1
                if(count==0):
                    self.captext_signal.emit("save it %s"%(picname))
                    cv2.imwrite(picname, frame)
                    break
                else:
                    continue
            cap.release()
            cv2.destroyAllWindows()
            self.captext_signal.emit(
                "Done, please check your progress !")


class imgThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal(str)
    imgtext_signal = QtCore.pyqtSignal(str)
    progmax_signal = QtCore.pyqtSignal(int)
    progvalue_signal = QtCore.pyqtSignal(int)

    def __init__(self, txtname, imgfile):
        super().__init__()
        self.txtname = txtname
        self.imgfile = imgfile
        self.api = Spiders()

    def run(self):
        start = time.time()
        self.status_signal.emit("当前状态：正在进行批量下载图片操作...")
        if os.path.isfile(self.txtname):  # 如果文件存在
            if not os.path.isdir(self.imgfile):
                try:
                    os.mkdir(self.imgfile)
                    self.imgtext_signal.emit(self.api.getmsg(
                        "创建一个新的文件夹，名称为   {}".format(self.imgfile), "green"))
                except:
                    self.imgfile = "PICs"
                    msg_a = "输入的文件夹名称不合格，使用默认文件夹：  {}".format(self.imgfile)
                    self.imgtext_signal.emit(self.api.getmsg(msg_a, "red"))
                    try:
                        os.mkdir(self.imgfile)
                    except:
                        pass
            infos = self.api.get_Infos(self.txtname)
            newinfos = [x for x in infos if "," in x and len(x) > 3]  # 只要有效链接
            num = len(newinfos)
            self.progmax_signal.emit(num)
            msg_b = '获取有效图片链接总计{}个，开始批量下载图片...'.format(num)
            self.imgtext_signal.emit(self.api.getmsg(msg_b, "#464749"))
            i = 1
            for each in newinfos:
                savename = each.split(",")[0]
                imgurl = each.split(",")[1]
                try:
                    self.api.downimg(self.imgfile, savename, imgurl)
                except:
                    bugmsg = '第{}个图片链接：{}   下载失败！'.format(i, imgurl)
                    self.imgtext_signal.emit(self.api.getmsg(bugmsg, "red"))
                else:
                    msg_c = "正在下载第{}个图片，保存为：{}".format(i, savename)
                    self.imgtext_signal.emit(self.api.getmsg(msg_c, "#464749"))
                self.progvalue_signal.emit(i)
                i += 1
            end = time.time()
            msg_d = "图片批量下载完毕，耗时：%0.2f秒！\n所有图片保存在文件夹  %s  中" % (
                float(end - start), self.imgfile)
            self.imgtext_signal.emit(self.api.getmsg(msg_d, "green"))
        else:
            themsg2 = '文件不存在，请创建文件再操作！'
            self.imgtext_signal.emit(self.api.getmsg(themsg2, "red"))
        self.status_signal.emit("当前状态：批量下载图片操作完毕！")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myui = MainUI()
    myui.show()
    sys.exit(app.exec_())
