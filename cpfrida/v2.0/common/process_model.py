# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/03/16
# @Author  : XQE
# @Software: PyCharm


import os
import psutil
import configparser


class Process(object):
    """
    进程管理
    """
    kill_cmd = "kill -9 {}"
    pro_path = "Process"
    pro_conf = configparser.ConfigParser()
    monitor_conf = configparser.ConfigParser()

    def __init__(self, filename, device, monitor_file="", full_path=""):
        """
        初始化
        :param filename : 工作空间
        :param device : 业务线
        :param monitor_file : 监控文件
        :param full_path : 完成路径
        """
        self.pid = os.getpid()
        self.process_filename = filename
        self.process_device = device
        self.monitor_file = monitor_file
        self.pro_path = os.path.join(full_path, self.pro_path)
        self.worker = os.path.join(os.path.join(full_path, self.process_filename), self.process_filename + ".py")
        self._check_process()
        self._record_process(self.read_pro_conf(self.process_filename))

    def _check_process(self):
        """
        检测进程文件夹
        """
        if os.path.exists(self.pro_path) is False:
            try:
                os.makedirs(self.pro_path)
            except Exception as e:
                pass

    def read_pro_conf(self, devices=None):
        """
        读取进程文件
        :param devices : 进程文件名
        return 进程文件对象
        """
        if devices:
            conf_file = os.path.join(self.pro_path, devices + '.conf')
        else:
            conf_file = os.path.join(self.pro_path, self.process_filename + '.conf')
        self.pro_conf.read(conf_file, encoding='utf-8')
        return conf_file

    def _record_process(self, conf_file):
        """
        记录python脚本运行记录
        """
        if os.path.exists(os.path.join(self.pro_path, self.process_filename)) is False:
            try:
                self.pro_conf.add_section('process')
            except Exception as e:
                pass
            self.pro_conf['process']['filename'] = self.process_filename
            self.pro_conf['process']['path'] = self.worker
            self.pro_conf['process']['exe'] = str(psutil.Process(self.pid).cmdline()[0])
            self.pro_conf['process']['script'] = self.process_filename + ".py"
            self.pro_conf.write(open(conf_file, 'w', encoding='utf-8'), space_around_delimiters=False)

    def read_monitor_conf(self):
        """
        读取监控进程文件
        """
        self.monitor_conf.read(self.monitor_file, encoding='utf-8')

    def remove_monitor_conf(self):
        """
        将异常的设备剔除出运维名单
        """
        self.read_monitor_conf()
        self.monitor_conf.remove_option("devices", self.process_filename)
        self.monitor_conf.write(open(self.monitor_file, 'w', encoding='utf-8'), space_around_delimiters=False)
        self.kill_process()

    def kill_process(self, pid=None):
        """
        杀死当前python脚本
        :param pid : 进程ID
        """
        self.read_pro_conf(pid)
        if pid is None:
            os.system(self.kill_cmd.format(str(self.pid)))
        else:
            os.system(self.kill_cmd.format(str(pid)))

    @staticmethod
    def restart_process(cmd):
        """
        重启进程
        :param cmd : 进程启动指令
        """
        os.system(cmd)

