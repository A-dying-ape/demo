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

import sys
import time
import frida
import random
import config
import control
import requests

sys.path.append("../common")
sys.path.append("../../common")
from logging_model import Logging
from process_model import Process
from ident_model import Ident
from phone_model import Phone
from thread_model import VxThread


class BaseScript(Logging, Process, Ident, Phone, VxThread):
    # 一次完整hook的标记
    flag = False
    # 当前业务线
    device = ""
    # 等待倒计时
    wait_count = 0
    # frida对象
    frida_object = None
    # hook参数
    get_response = dict()
    # 回调数据
    post_response = dict()
    # 风控标记
    risk_control_flag = False

    def __init__(
            self,
            filename,
            full_path=""
    ):
        """
        初始化对象：
        :param filename: 工作空间文件名
        :param full_path: 完整路径
        """
        self.filename = filename
        self.timeout = config.timeout
        self.frida_host = config.frida_host
        self.app_name_en = config.app_name_en
        self.app_name_ch = config.app_name_ch
        self.hook_script = config.hook_script
        Logging.__init__(self, filename, full_path)
        Process.__init__(self, filename, "../monitor/monitor_conf.ini", full_path)
        Ident.__init__(self, filename, full_path)
        Phone.__init__(self, config.adb_host, self.app_name_en, config.app_ui)
        VxThread.__init__(self, control.business_sleep_time)
        self.addr = self.get_host_ip()
        self.uuid = self.get_workspace_uuid()

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
                        self.logger.info("restart app ......")
                        self.restart_app(stop_time=control.stop_app_time, restart_time=control.restart_app_time, connect_time=control.connect_phone_time)
                        time.sleep(control.each_create_frida_time)
        try:
            with open(self.hook_script, encoding="utf-8") as f:
                script = session.create_script(f.read(), runtime="v8")
                script.on("message", self.my_message_handler)
                script.load()
                self.logger.info("hook script success.")
                return script
        except Exception as e:
            self.logger.error("frida create script fail: " + str(e), exc_info=False)

    def unload_frida(self):
        """
        卸载脚本
        :return:
        """
        try:
            self.logger.info("unload frida ......")
            self.frida_object.unload()
        except Exception as e:
            self.logger.error("frida object unload fail: " + str(e), exc_info=False)
        self.frida_object = None

    def wait(self):
        """
        限时等待js响应
        """
        self.wait_count = 0
        self.flag = False
        while True:
            time.sleep(control.refresh_js_time)
            self.wait_count += 1
            if self.flag or self.wait_count > self.timeout / control.refresh_js_time:
                if self.wait_count > self.timeout / control.refresh_js_time:
                    self.logger.info("hook time out ......")
                    self.unload_frida()
                    self.logger.info("restart app ......")
                    self.restart_app()
                self.flag = False
                break

    def get_params(self):
        """
        获取队列消息
        """
        while True:
            try:
                self.get_response = {}
                for dev, url in config.get_url.items():
                    if dev in self.shield_business:
                        continue
                    self.get_response = requests.get(url.format(self.uuid, self.addr))
                    self.get_response.encoding = "utf-8"
                    self.get_response = self.get_response.json()
                    self.logger.info(self.get_response)
                    if self.get_response.get("code") == 0:
                        self.device = dev
                        self.logger.info("the current business: %s" % dev)
                        break
                if self.get_response.get("code") == 0:
                    break
                else:
                    self.logger.info("The same delay interface does not allow uninterrupted operation.")
                time.sleep(control.get_hook_params_time)
            except Exception as e:
                self.logger.error("params queue closed: " + str(e), exc_info=False)
