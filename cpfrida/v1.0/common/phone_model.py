# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/15
# @Author  : XQE
# @Software: PyCharm


import os
import time


class Phone(object):
    """
    设备模块
    """
    adb_connect = "adb connect {}"
    adb_stop = "adb -s {} shell am force-stop {}"
    adb_start = "adb -s {} shell am start {}"
    adb_reboot = "adb -s {} reboot"
    adb_screen_bright = 'adb -s {} shell settings put system screen_brightness {}'

    def __init__(self, host, app="", ui=""):
        """
        初始化
        :param host : adb远端IP端口
        :param app : 包名
        :param ui : 主界面
        """
        assert host, "host is not \"\""
        self.adb_start = self.adb_start.format(host, ui)
        self.adb_stop = self.adb_stop.format(host, app)
        self.adb_screen_bright = self.adb_screen_bright.format(host, "{}")
        self.adb_connect = self.adb_connect.format(host)
        self.adb_reboot = self.adb_reboot.format(host)

    def set_screen_bright(self, bright=1):
        """
        屏幕亮度最低
        :param bright : 亮度值
        """
        self._connect()
        os.system(self.adb_screen_bright.format(bright))

    def _connect(self, host=None):
        """
        adb 连接
        """
        os.system("adb connect {}".format(host)) if host else os.system(self.adb_connect)
        time.sleep(1)

    def restart_app(self):
        """
        重启app
        """
        self._connect()
        os.system(self.adb_stop)
        time.sleep(1)
        os.system(self.adb_start)
        time.sleep(15)

    def reboot(self, host=None):
        """
        重启手机
        """
        self._connect(host)
        if host:
            os.system("adb -s {} reboot".format(host))
        else:
            os.system(self.adb_reboot)
        time.sleep(2)
