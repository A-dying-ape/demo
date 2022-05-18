# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/05/18
# @Author  : XQE
# @Software: PyCharm


class Communicate(object):
    """
    进程间的通讯模块
    """
    # 是否回复
    is_reply = False

    def __init__(self, notice_queue, reply_queue):
        """
        初始化
        :param notice_queue: 进程通知队列
        :param reply_queue: 进程回复队列
        """
        self.notice_queue = notice_queue
        self.reply_queue = reply_queue

    def put_notice_queue(self, value):
        """
        通知队列添加值
        :param:value: 队列消息
        :return:
        """
        self.notice_queue.put(value)

    def put_reply_queue(self, value):
        """
        回复队列添加值
        :param:value: 队列消息
        :return:
        """
        self.reply_queue.put(value)

    def get_notice_queue(self):
        """
        获取通知队列值
        :return:值
        """
        return self.notice_queue.get()

    def get_reply_queue(self):
        """
        获取回复队列值
        :return:值
        """
        return self.reply_queue.get()

    def notice_is_empty(self):
        """
        判断通知队列是否为空
        :return: bool
        """
        return self.notice_queue.empty()

    def reply_is_empty(self):
        """
        判断回复队列是否为空
        :return: bool
        """
        return self.reply_queue.empty()

    def clear_notice_queue(self):
        while True:
            if self.notice_is_empty():
                break
            else:
                self.get_notice_queue()

    def clear_reply_queue(self):
        while True:
            if self.reply_is_empty():
                break
            else:
                self.get_reply_queue()