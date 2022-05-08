# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


"""
整个采集脚本的基础类
完整的流程：
1.hook加载类(js加载数据)
2.hook数据类(js获取数据)
"""

import re
import sys
import time
import frida
import config
import requests
sys.path.append("../common")
sys.path.append("../../common")
from logging_model import Logging
from process_model import Process
from ident_model import Ident
from phone_model import Phone


class BaseScript(Logging, Process, Ident, Phone):
    flag = False
    device = ""
    wait_count = 0
    frida_object = None
    get_response = dict()
    post_response = dict()
    remove_monitor = False

    def __init__(self, filename, device, url, full_path=""):
        """
        初始化对象：
        :param filename : 工作空间文件名
        :param full_path : 完整路径
        """
        self.device = device
        self.filename = filename
        self.timeout = config.timeout
        self.frida_host = config.frida_host
        self.app_name_en = config.app_name_en
        self.app_name_ch = config.app_name_ch
        self.hook_script = config.hook_script
        Logging.__init__(self, filename, device, full_path)
        Process.__init__(self, filename, device + re.search(r"\d+", filename).group(), "../monitor/monitor_conf.ini", full_path)
        Ident.__init__(self, filename, full_path)
        Phone.__init__(self, config.adb_host, self.app_name_en, config.app_ui)
        self.addr = self.get_host_ip()
        self.uuid = self.get_workspace_uuid()
        self.get_params_url = url

    def check_frida(self):
        """
        检测frida
        """
        if self.frida_object is None:
            self.frida_object = self.session()

    def session(self):
        """
        frida远程植入微信进程
        :return: 植入载体
        """
        session = None
        while session is None:
            device = None
            try:
                manager = frida.get_device_manager()
                device = manager.add_remote_device(self.frida_host)
            except Exception as e:
                self.logger.error("frida connect fail: " + str(e), exc_info=False)
            if device is not None:
                try:
                    session = device.attach(self.app_name_en)
                    self.logger.info("frida attach appname %s" % self.app_name_en)
                except Exception as e:
                    self.logger.error("frida attach %s fail: " % self.app_name_en + str(e), exc_info=False)
                    try:
                        session = device.attach(self.app_name_ch)
                        self.logger.info("frida attach appname %s" % self.app_name_ch)
                    except Exception as e:
                        self.logger.error("frida attach %s fail: " % self.app_name_ch + str(e), exc_info=False)
                        time.sleep(5)
        try:
            with open(self.hook_script, encoding="utf-8") as f:
                script = session.create_script(f.read(), runtime="v8")
                script.on("message", self.my_message_handler)
                script.load()
                self.logger.info("hook script success.")
                return script
        except Exception as e:
            self.logger.error("frida create script fail: " + str(e), exc_info=False)

    def wait(self):
        """
        限时等待js响应
        """
        self.wait_count = 0
        self.flag = False
        while True:
            time.sleep(0.1)
            self.wait_count += 1
            if self.flag or self.wait_count > self.timeout:
                if self.wait_count > self.timeout:
                    self.logger.info("hook time out ...")
                    # 当存在风控风险时重启设备
                    if self.remove_monitor:
                        self.logger.info("reboot phone ...")
                        self.reboot()
                    if self.frida_object:
                        self.frida_object.unload()
                    break
                self.flag = False
                break

    def get_params(self):
        """
        获取队列消息
        """
        while True:
            try:
                self.get_response = requests.get(self.get_params_url.format(self.uuid, self.addr))
                self.get_response.encoding = "utf-8"
                self.get_response = self.get_response.json()
                self.logger.info(self.get_response)
                if self.get_response.get("code") == 0:
                    self.logger.info("the current business: %s" % self.device)
                    break
                time.sleep(1)
            except Exception as e:
                self.logger.error("params queue closed: " + str(e), exc_info=False)
