# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import sys
import time
import psutil
import platform
import telnetlib
sys.path.append("../../common")
from logging_model import Logging
from phone_model import Phone
from process_model import Process


class Monitor(Logging, Phone, Process):
    """
    所有的工作空间监控和自动化运维
    """

    def __init__(self, filename="monitor", full_path=".."):
        """
        初始化对象
        :param filename : 文件名
        :param full_path : 完整路径
        """
        self.full_path = full_path
        Logging.__init__(self, "", "monitor", self.full_path)
        Phone.__init__(self, filename, self.full_path)
        Process.__init__(self, filename, "monitor", monitor_file="monitor_conf.ini", full_path=self.full_path)
        self.read_monitor_conf()

    def get_all_devices(self):
        """
        获取所有的设备
        :return 设备列表
        """
        return self.monitor_conf.options("devices")

    def check_local_pro(self):
        """
        检测工作单位的本地进程
        :return 异常的进程
        """
        err_pro = []
        self.read_monitor_conf()
        for d in self.get_all_devices():
            self.read_pro_conf(d)
            try:
                process = psutil.Process(int(self.pro_conf["process"]["pid"]))
                if "python" in process.cmdline()[0] and d in process.cmdline()[1]:
                    create_time = process.create_time()
                    curr_time = time.time()
                    if int(curr_time - create_time) > 60 * 60 * 6:
                        err_pro.append(d)
                        continue
                else:
                    self.logger.error("%s is not run python ." % d)
                    err_pro.append(d)
            except Exception as e:
                self.logger.error("%s is not run" % d + ": " + str(e), exc_info=False)
                err_pro.append(d)
        return err_pro

    def handle_devices(self, devices):
        """
        处理异常的设备
        :return 处理成功的设备
        """
        start_cmd = []
        for device in devices:
            self.read_pro_conf(device)
            while True:
                try:
                    self.reboot(self.monitor_conf["devices"][device])
                    if platform.system() == 'Windows':
                        start_cmd.append(str(self.pro_conf["process"]["exe"]) + " " + str(self.pro_conf["process"]["path"]))
                    elif platform.system() == 'Linux':
                        start_cmd.append("nohup " + str(self.pro_conf["process"]["exe"]) + " -u " + str(self.pro_conf["process"]["path"]) + " >/dev/null 2>&1 &")
                    else:
                        raise Exception("unknown system.")
                    break
                except Exception as e:
                    self.reboot(self.monitor_conf["devices"][device])
                    self.logger.error("kill process %s fail " % str(self.pro_conf["process"]["pid"]) + " : " + str(e), exc_info=False)
            self.logger.info("reboot devices done: " + str(device))
        return start_cmd

    def check_telnet(self, down_devices):
        """
        检测当前要处理的设备frida端口是否联通
        :param down_devices: 设备列表
        :return: 联通的设备列表
        """
        devices_list = list()
        for d in down_devices:
            ip = self.monitor_conf["devices"][d].split(":")[0]
            port = int("104" + self.monitor_conf["devices"][d].split(":")[1][3:])
            try:
                telnetlib.Telnet(ip, port, 2)
                devices_list.append(d)
            except Exception as e:
                pass
        return devices_list