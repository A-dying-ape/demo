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
    adb_disconnect = "adb disconnect {}"
    adb_stop = "adb -s {} shell am force-stop {}"
    adb_start = "adb -s {} shell am start {}"
    adb_reboot = "adb -s {} shell reboot system"
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
        self.adb_disconnect = self.adb_disconnect.format(host)
        self.adb_reboot = self.adb_reboot.format(host)

    def set_screen_bright(self, bright=1):
        """
        屏幕亮度最低
        :param bright : 亮度值
        """
        self._connect()
        os.system(self.adb_screen_bright.format(bright))

    def _connect(self, host=None, connect_time=2):
        """
        adb 连接
        """
        os.system("adb connect {}".format(host)) if host else os.system(self.adb_connect)
        time.sleep(connect_time)

    def _disconnect(self, host=None, connect_time=2):
        os.system("adb disconnect {}".format(host)) if host else os.system(self.adb_disconnect)
        time.sleep(connect_time)

    def restart_app(self, host=None, app="com.tencent.mm", ui="com.tencent.mm/com.tencent.mm.ui.LauncherUI", stop_time=2, restart_time=7, connect_time=2):
        """
        重启app
        """
        if host:
            self._connect(host=host, connect_time=connect_time)
            os.system("adb -s {} shell am force-stop {}".format(host, app))
            time.sleep(stop_time)
            os.system("adb -s {} shell am start {}".format(host, ui))
            time.sleep(restart_time)
            self._disconnect(host=host, connect_time=connect_time)
        else:
            self._connect(connect_time=connect_time)
            os.system(self.adb_stop)
            time.sleep(stop_time)
            os.system(self.adb_start)
            time.sleep(restart_time)
            self._disconnect(connect_time=connect_time)

    def reboot(self, host=None, reboot_time=60, connect_time=2):
        """
        重启手机
        """
        if host:
            self._connect(host=host, connect_time=connect_time)
            os.system("adb -s {} reboot".format(host))
            self._disconnect(host=host, connect_time=connect_time)
        else:
            self._connect(connect_time=connect_time)
            os.system(self.adb_reboot)
            self._disconnect(connect_time=connect_time)
        time.sleep(reboot_time)

