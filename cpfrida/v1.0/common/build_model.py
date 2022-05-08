# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/15
# @Author  : XQE
# @Software: PyCharm


import os
import configparser


class Build(object):
    """
    build.ini文件相关操作
    """
    config_path = "../deploy/build.ini"
    build_config = None

    def __init__(self):
        """
        初始化
        """
        assert self._check_config(self.config_path), "'build.ini' is not in the deploy directory."
        self.build_config = configparser.ConfigParser()

    @staticmethod
    def _check_config(path):
        """
        检测目录下是否存在build.ini文件
        :param path : 检测的目录
        """
        return os.path.exists(path)

    def read_config(self):
        """
        读取build.ini
        """
        self.build_config.read("build.ini", encoding="utf-8")

    def write_config(self):
        """
        写入build.ini
        """
        self.build_config.write(open('../deploy/build.ini', 'w', encoding='utf-8'), space_around_delimiters=False)
