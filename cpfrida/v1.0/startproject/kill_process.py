# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/08
# @Author  : XQE
# @Software: PyCharm


"""
项目部署时要杀死所有相关的进程
"""


import os
import sys
import configparser


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


def read_process():
    """
    读取项目下的所有进程配置文件
    :return: 完整的进程配置文件路径  list
    """
    process_path = os.path.join(os.path.join(read_conf("../deploy/build.ini")["project"]["path"], "workspaces"), "Process")
    if os.path.exists(process_path) is False:
        os.mkdir(process_path)
    return [os.path.join(process_path, file) for file in os.listdir(process_path)]


def kill_pid():
    """
    杀死所有的进程
    :return:
    """
    for process in read_process():
        conf = read_conf(process)
        if conf:
            pid = conf["process"]["pid"]
            os.system("kill -9 %s" % pid)


if __name__ == '__main__':
    kill_pid()
    sys.exit(0)
