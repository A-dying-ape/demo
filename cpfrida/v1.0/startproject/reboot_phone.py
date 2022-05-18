# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/02/23
# @Author  : XQE
# @Software: PyCharm


"""
项目部署是要重启所有的手机
"""


import os
import time
import queue
import platform
import configparser
import multiprocessing
from multiprocessing import Queue


project_path = "/wechatserver/wxhook"
adb_connect = 'adb connect {}'
adb_disconnect = 'adb disconnect {}'
adb_reboot = 'adb -s {} reboot'


def read_conf(config_path):
    """
    读取配置文件
    :param config_path:配置文件路径
    :return:配置文件
    """
    config = None
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
    except Exception as e:
        print("no configuration file " + str(e))
    return config


def reboot(conf, queue):
    """
    重启所有的设备
    :param conf: 配置文件
    :param queue: 设备队列
    :return:
    """
    while True:
        if queue.empty():
            break
        device = queue.get()
        rbc = 1
        while True:
            try:
                if rbc >= 5:
                    break
                os.system(adb_connect.format(conf['devices'][device]))
                time.sleep(2)
                os.system(adb_reboot.format(conf['devices'][device]))
                time.sleep(2)
                os.system(adb_disconnect.format(conf['devices'][device]))
                break
            except Exception as e:
                rbc += 1
                print("reboot devices fail " + str(rbc) + " : " + str(e))
        print(device + "重启完成 ！")


if __name__ == '__main__':
    monitor_conf = os.path.join(os.path.join(os.path.join(project_path, "workspaces"), "monitor"), "monitor_conf.ini")
    conf = read_conf(monitor_conf)
    queues = Queue()
    for device in conf.options('devices'):
        queues.put(device)
    mul_list = []
    for i in range(10):
        mul_list.append(multiprocessing.Process(target=reboot, args=(conf, queues,)))
    for mul in mul_list:
        mul.start()
