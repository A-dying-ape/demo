# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/19
# @Author  : XQE
# @Software: PyCharm


import json
import requests


class Inform(object):
    """
    消息通知模块
    """
    inform_headers = {'Content-Type': 'application/json;charset=utf-8'}

    def __init__(self, inform_url):
        """
        初始化
        :param inform_url : 消息发送的地址
        """
        self.inform_url = inform_url

    def inform(self, inform_text):
        """
        通知消息
        :param inform_text : 发送的消息
        :return 状态
        """
        status = requests.post(
            self.inform_url,
            json.dumps(inform_text),
            headers=self.inform_headers,
            verify=False
        ).content
        return status
