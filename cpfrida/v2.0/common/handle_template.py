# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/15
# @Author  : XQE
# @Software: PyCharm


import re
import os
from build_model import Build


class FormatTemplate(Build):
    """
    初始化模板
    """
    def __init__(self):
        Build.__init__(self)
        self.read_config()

    @staticmethod
    def _check_template(content):
        """
        检测当前模板是否需要格式化
        :param content 模板内容
        :return bool
        """
        try:
            return re.search(r"\{\$\w+\$\}", content).group(0)
        except Exception as e:
            print("模板错误")
            return False

    @staticmethod
    def _begin_format(target, value, content):
        """
        格式化模板
        :param target : 模板准备替换的标识
        :param value : 替换的值
        :param content : 模板内容
        :return 替换后的模板
        """
        return re.sub(r"\{\$" + target + r"\$\}", value, content)

    def format_template(self, devices, template):
        """
        匹配工作空间对应的全局配置文件
        :param devices : 工作空间
        :param template : 模板
        :return 格式化后的代码
        """
        with open(os.path.join("../deploy/template", template), "r", encoding="utf-8") as f:
            content = f.read()
        assert self._check_template(content), "'%s' Template error, Check whether the template should be replaced with '{$  $}'." % template
        targets = self.build_config.options(devices)
        for target in targets:
            content = self._begin_format(target, self.build_config[devices].get(target), content)
        if "{$project_path$}" in content:
            content = self._begin_format("project_path", self.build_config["project"].get("path"), content)
        return content

