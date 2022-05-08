# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/16
# @Author  : XQE
# @Software: PyCharm

import os
import uuid
import socket


class Ident(object):
    """
    创建或获取工作空间的标识
    """
    uuid_file = "uuid"
    work_path = ""

    def __init__(self, filename, full_path=""):
        """
        初始化
        :param filename : 工作空间
        :param full_path : 完成路径
        """
        self.filename = filename
        self.work_path = os.path.join(full_path, filename)
        assert self._check_workspace(), "%s workspace does not exist" % self.work_path
        self.uuid_file = os.path.join(self.work_path, self.uuid_file)

    def _check_workspace(self):
        """
        检测工作空间
        :return: bool
        """
        return os.path.exists(self.work_path)

    @staticmethod
    def get_host_ip():
        """
        获取本地IP
        :return: 本地IP
        """
        ip = ""
        st = None
        try:
            st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            st.connect(('8.8.8.8', 80))
            ip = st.getsockname()[0]
        except Exception as e:
            pass
        finally:
            st.close()
            return ip

    def get_workspace_uuid(self):
        """
        获取或生成机器标识码  UUID4
        :return: 机器标识码
        """
        if not os.path.exists(self.uuid_file):
            with open(self.uuid_file, 'w', encoding='utf-8') as f:
                workers_uuid = str(uuid.uuid4())
                f.write(workers_uuid)
        else:
            with open(self.uuid_file, "r") as f:
                workers_uuid = f.read().strip()
        return workers_uuid
