from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import os
import get_cookies
import monitor


proxy_flag = False


class CookieThread(QThread):
    update_log = pyqtSignal(str)
    login_count = pyqtSignal(str)
    account_list = None

    def run(self):
        get_cookies.run_cookie(self.account_list, self.update_log, self.login_count)


class MonitorThread(QThread):
    updata_log = pyqtSignal(str)
    url = None
    spike_count = pyqtSignal(str)

    def run(self):
        global proxy_flag
        monitor.run_login(self.url, self.updata_log, proxy_flag, self.spike_count)


class DrawView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("淘宝秒杀系统v1.0")
        self.resize(800, 600)
        self.initUI()

    def initUI(self):
        # 导入登陆button
        self.ia_btn = QPushButton(self)
        self.ia_btn.setText("批量登陆账号")
        self.ia_btn.setGeometry(30, 30, 180, 40)
        self.ia_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.ia_btn.setFont(QFont("Arial", 16))
        self.ia_btn.clicked.connect(self.loadText)
        # 账号总数label
        self.ia_label1 = QLabel(self)
        self.ia_label1.setGeometry(38, 78, 180, 20)
        self.ia_label1.setText("导入账号总数:<font color=red> %s</font>" % 0)
        self.ia_label1.setFont(QFont("Arial", 11))
        # 抢购成功label
        self.ia_label2 = QLabel(self)
        self.ia_label2.setGeometry(38, 104, 180, 20)
        self.ia_label2.setText("抢购成功账号总数:<font color=red> %s</font>" % 0)
        self.ia_label2.setFont(QFont("Arial", 11))
        # 秒杀button
        self.su_btn = QPushButton(self)
        self.su_btn.setText("开始秒杀")
        self.su_btn.setGeometry(30, 130, 180, 40)
        self.su_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.su_btn.setFont(QFont("Arial", 16))
        self.su_btn.clicked.connect(self.doSpikeGoods_load)
        self.su_btn.clicked.connect(self.doSpikeGoods)
        # 秒杀进度label
        self.su_label = QLabel(self)
        self.su_label.setText("读取账号信息...")
        self.su_label.setGeometry(38, 180, 180, 20)
        self.su_label.setFont(QFont("Arial", 11))
        # 进度条progressbar
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 200, 210, 30)
        # 设置进度条初始值
        self.step = 0
        # 设置定时器
        self.timer = QBasicTimer()
        # 清除cookie
        self.ck_btn = QPushButton(self)
        self.ck_btn.setText("清除cookie")
        self.ck_btn.setGeometry(30, 310, 180, 40)
        self.ck_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.ck_btn.setFont(QFont("Arial", 16))
        self.ck_btn.clicked.connect(self.clearCookie)
        # 清除账号
        self.ac_btn = QPushButton(self)
        self.ac_btn.setText("清除账号")
        self.ac_btn.setGeometry(30, 380, 180, 40)
        self.ac_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.ac_btn.setFont(QFont("Arial", 16))
        self.ac_btn.clicked.connect(self.clearAccount)
        # 清除日志
        self.lg_btn = QPushButton(self)
        self.lg_btn.setText("清除日志")
        self.lg_btn.setGeometry(30, 450, 180, 40)
        self.lg_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.lg_btn.setFont(QFont("Arial", 16))
        self.lg_btn.clicked.connect(self.onClearLog)
        # 导入代理IP
        self.ip_btn = QPushButton(self)
        self.ip_btn.setText("启用代理IP")
        self.ip_btn.setGeometry(30, 520, 180, 40)
        self.ip_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.ip_btn.setFont(QFont("Arial", 16))
        self.ip_btn.clicked.connect(self.setProxy)
        # 请输入网址
        self.url_label = QLabel(self)
        self.url_label.setGeometry(260, 30, 180, 20)
        self.url_label.setText("请输入网址:")
        self.url_label.setFont(QFont("Arial", 14))
        # 网址输入框
        self.url_ed = QLineEdit(self)
        self.url_ed.setGeometry(370, 25, 330, 30)
        # 重置按钮
        self.re_btn = QPushButton(self)
        self.re_btn.setText("重置")
        self.re_btn.setGeometry(720, 22, 70, 35)
        self.re_btn.setStyleSheet("QPushButton{background-color:rgb(255,255,255)}")
        self.re_btn.setFont(QFont("Arial", 16))
        self.re_btn.clicked.connect(self.onClearText)
        # 日志label
        self.url_label = QLabel(self)
        self.url_label.setGeometry(260, 80, 180, 20)
        self.url_label.setText("日志信息:")
        self.url_label.setFont(QFont("Arial", 11))
        # 日志框
        self.lg_ed = QTextBrowser(self)
        self.lg_ed.setGeometry(240, 100, 560, 440)
        self.lg_ed.setFont(QFont("SumSin", 16))
        # 系统时间
        self.time_label = QLabel(self)
        self.time_label.setGeometry(420, 560, 300, 20)
        self.time_label.setText(
            "<font color='red'>系统时间:  %s</font>" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.time_label.setFont(QFont("Arial", 11))
        # 自定义QTimer
        self.Timer = QTimer()
        self.Timer.start(1000)
        self.Timer.timeout.connect(self.updateTime)

    def setProxy(self):
        global proxy_flag
        proxy_flag = True
        self.lg_ed.append(">>启用代理IP！")

    def clearCookie(self):
        if os.path.exists("cookies.txt"):
            os.remove("cookies.txt")
            self.lg_ed.append("已经清除所有cookie!")
        else:
            self.lg_ed.append("系统未检测到cookies！")

    def clearAccount(self):
        if os.path.exists("pay_pwd.txt"):
            os.remove("pay_pwd.txt")
            self.lg_ed.append("已经清除所有的账号信息!")
        else:
            self.lg_ed.append("系统未检测到账号信息文件！")

    def paintEvent(self, event):
        # 创建绘图
        painter = QPainter(self)
        painter.begin(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        # 实线1
        painter.setPen(pen)
        painter.drawLine(0, 270, 240, 270)
        # 实线2
        painter.setPen(pen)
        painter.drawLine(240, 0, 240, 600)
        painter.end()

    def timerEvent(self, *args, **kwargs):
        # 定时器
        if self.step >= 100:
            self.timer.stop()
            self.su_btn.setText('开始秒杀')
            self.su_btn.setEnabled(True)
            self.step = 0
            return
        else:
            self.step = self.step + 1
            self.pbar.setValue(self.step)

    def doSpikeGoods_load(self):
        # 秒杀进度条
        if self.timer.isActive():
            self.timer.stop()
            self.su_btn.setText('开始秒杀')
            self.su_btn.setEnabled(True)
        else:
            self.timer.start(100, self)
            self.su_btn.setText('秒杀中...')
            self.su_btn.setEnabled(False)

    def updateTime(self):
        self.time_label.setText("<font color='red'>系统时间:  %s</font>" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def onClearText(self):
        self.url_ed.clear()

    def onClearLog(self):
        self.lg_ed.clear()

    def loadText(self):
        content = QFileDialog()
        content.setFileMode(QFileDialog.AnyFile)
        content.setFilter(QDir.Files)
        if content.exec():
            filenames = content.selectedFiles()
            f = open(filenames[0], encoding="utf-8", mode="r")
            with f:
                data = f.read()
                self.lg_ed.setText(data)
        if data == "":
            self.lg_ed.append(">>未读取到账号，请检查导入文件%s" % filenames[0])
        else:
            self.back_cookie = CookieThread()
            self.back_cookie.account_list = data.split("\n")
            self.back_cookie.update_log.connect(self.show_log)
            self.back_cookie.login_count.connect(self.show_login_count)
            self.back_cookie.start()

    def show_log(self, log):
        self.lg_ed.append(log)

    def show_login_count(self, count):
        self.ia_label1.setText("导入账号总数:<font color=red> %s</font>" % count)

    def doSpikeGoods(self):
        url = self.url_ed.text()
        if url == '':
            self.lg_ed.append(">>请输入秒杀页面的url！")
        elif not (url.startswith("http://") or url.startswith("https://")):
            self.lg_ed.append(">>请输入有效秒杀页面的url！")
        else:
            self.back_monitor = MonitorThread()
            self.back_monitor.url = url
            self.back_monitor.updata_log.connect(self.show_log)
            self.back_monitor.spike_count.connect(self.show_skipe_count)
            self.back_monitor.start()

    def show_skipe_count(self, count):
        self.ia_label2.setText("抢购成功账号总数:<font color=red> %s</font>" % count)


def run():
    app = QApplication(sys.argv)
    main = DrawView()
    # 设置窗口背景色
    main.setObjectName("MainWindow")
    main.setStyleSheet("#MainWindow{background-color:#cacaca}")
    main.show()
    sys.exit(app.exec_())