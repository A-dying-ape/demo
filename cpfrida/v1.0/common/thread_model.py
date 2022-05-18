# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/05/18
# @Author  : XQE
# @Software: PyCharm
import time
import random
import threading


class VxThread(threading.Thread):
    """线程管理"""
    shield_business = set()

    def __init__(self, sleep_time):
        """
        初始化
        :param sleep_time: 业务流程控制对象
        """
        super(VxThread, self).__init__()
        self.sleep_time = sleep_time

    def vx_start_thread(self, device):
        """
        启动休眠线程
        :param device: 业务线
        :return:
        """
        threading.Thread(target=self.thread_sleep, args=(device,)).start()

    def thread_sleep(self, device):
        """
        线程休眠
        :param device: 业务线
        :return:
        """
        begin = self.sleep_time[device]["begin"]
        end = self.sleep_time[device]["end"]
        if begin > 0 or end > 0:
            self.shield_business.add(device)
            time.sleep(random.randint(begin, end))
            self.shield_business.remove(device)