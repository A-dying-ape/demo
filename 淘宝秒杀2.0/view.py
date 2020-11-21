from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import tkinter.messagebox as messagebox
from get_cookies import run_cookie
from monitor import run_login
import os


class Make_UI():
    def __init__(self, window):
        self.window = window
        # 设置页面大小
        self.window.title("淘宝抢单系统_v 1.0.1")
        self.window.maxsize(1510, 910)
        self.window.geometry("1500x900+10+10")
        self.label1 = tk.Label(self.window, text="账号文件名:", font=("楷体", 16, "bold"), width=12, height=2)
        self.account_pwd_entry = tk.Entry(self.window, width=80, show=None, bd=3)
        self.ap_button = tk.Button(self.window, text="登陆账号", bg="orange", font=("楷体", 12, "bold"), bd=4, width=11, height=1, command=self.account_path)
        self.canvas1 = Canvas(window, bg="black", width=3, height=81)
        self.delete_cookie = tk.Button(self.window, text="清除cookie", bg="orange", font=("楷体", 12, "bold"), bd=4, width=11, height=1, command=self.clear_cookie)
        self.delete_account = tk.Button(self.window, text="清除支付密码", bg="orange", font=("楷体", 12, "bold"), bd=4, width=11, height=1, command=self.delete_user)
        self.canvas2 = Canvas(window, bg="black", width=1480, height=3)
        self.label2 = tk.Label(self.window, text="抢购网址:", font=("楷体", 16, "bold"), width=12, height=2)
        self.url_entry = tk.Entry(self.window, width=80, show=None, bd=3)
        self.ue_button = tk.Button(self.window, text="开始抢购", bg="orange", font=("楷体", 12, "bold"), bd=4, width=11, height=1, command=self.begin_action)
        self.canvas3 = Canvas(window, bg="black", width=3, height=81)
        self.clear_log = tk.Button(self.window, text="清空日志", bg="orange", font=("楷体", 12, "bold"), bd=4, width=11, height=1, command=self.delete_log)
        self.label3 = tk.Label(self.window, text="日志信息:", font=("楷体", 12, "bold"), width=12, height=2)
        self.log_text = tk.scrolledtext.ScrolledText(self.window, show=None, font=("楷体", 16), width=132, height=32, bd=4)

    def decorate_page(self):
        self.label1.place(x=20, y=20)
        self.ap_button.place(x=760, y=27)
        self.account_pwd_entry.place(x=170, y=33)
        self.delete_cookie.place(x=1150, y=27)
        self.delete_account.place(x=1310, y=27)
        self.canvas1.place(x=1000, y=10)
        self.canvas2.place(x=10, y=90)
        self.label2.place(x=31, y=130)
        self.url_entry.place(x=170, y=140)
        self.ue_button.place(x=760, y=135)
        self.canvas3.place(x=1000, y=95)
        self.clear_log.place(x=1150, y=135)
        self.label3.place(x=10, y=175)
        self.log_text.place(x=18, y=205)

    def account_path(self):
        path = self.account_pwd_entry.get()
        if path == '':
            messagebox.showwarning(title="提示", message="请输入文件名！")
        else:
            if os.path.exists(path):
                run_cookie(path, messagebox, self.log_show)
            else:
                messagebox.showwarning(title="提示", message="%s文件不存在！" % path)

    def clear_cookie(self):
        if os.path.exists("cookies.txt"):
            os.remove("cookies.txt")
            tip = "已经清除所有cookie!"
            self.log_show(tip)
        else:
            tip = "系统未检测到cookies！"
            self.log_show(tip)

    def delete_user(self):
        if os.path.exists("pay_pwd.txt"):
            os.remove("pay_pwd.txt")
            tip = "已经清除所有的支付密码!"
            self.log_show(tip)
        else:
            tip = "系统未检测到账号信息文件！"
            self.log_show(tip)

    def delete_log(self):
        self.log_text.delete(1.0, 'end')

    def begin_action(self):
        url = self.url_entry.get()
        if url == '':
            messagebox.showwarning(title="提示", message="请输入网址！")
        elif url.startswith("http://") or url.startswith("https://"):
            run_login(url, self.log_show, messagebox)
        else:
            messagebox.showwarning(title="提示", message="无效网址，请核对！")

    def log_show(self, text):
        text = "-->" + text + "\n"
        self.log_text.insert("end", text)