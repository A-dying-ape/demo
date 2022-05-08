# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/15
# @Author  : XQE
# @Software: PyCharm


import os
import logging
from logging.handlers import TimedRotatingFileHandler


class Logging(object):
    """
    日志模块
    """
    log_path = "Logs"
    when = "MIDNIGHT"
    backupCount = 7
    logger = logging.getLogger()

    def __init__(self, filename, device, full_path=""):
        """
        初始化
        :param filename : 工作空间
        :param full_path : 完成路径
        """
        self.logger_filename = filename
        self.log_path = os.path.join(os.path.join(os.path.join(full_path, self.log_path), self.logger_filename), device)
        self.log_file = str(device) + '.log'
        self._check_log()
        self._export_log()

    def _check_log(self):
        """
        检测日志文件夹
        """
        if os.path.exists(self.log_path) is False:
            os.makedirs(self.log_path)

    def _export_log(self):
        """
        格式化日志格式，一天一个日志文件
        """
        self.logger.setLevel(logging.INFO)
        fh = TimedRotatingFileHandler(filename=os.path.join(self.log_path, self.log_file), when=self.when, backupCount=self.backupCount, encoding="utf-8")
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

