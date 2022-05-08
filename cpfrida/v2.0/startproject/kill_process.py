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
import time
import psutil
import platform


kill_cmd_lin = "kill -9 {}"
kill_cmd_win = "taskkill /PID {} -f"


def kill_pid():
    """
    杀死所有的进程
    :return:
    """
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if "python" in p.name() and "kill_process" not in p.cmdline()[1]:
            if platform.system() == 'Windows':
                os.system(kill_cmd_win.format(pid))
            elif platform.system() == 'Linux':
                os.system(kill_cmd_lin.format(pid))
            else:
                raise Exception("unknown system.")
            time.sleep(1)


if __name__ == '__main__':
    kill_pid()
    sys.exit(0)



