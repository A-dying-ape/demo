# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/02/23
# @Author  : XQE
# @Software: PyCharm


"""
整个采集项目的启动入口
兼容windows和linux系统
"""


import os
import configparser


cmd_str = r"""#!/bin/bash

source /etc/profile
echo "============================== Linux deploy start ! =============================="
crontab -l | grep -v '{project_path}/workspaces/monitor' | crontab -
python3.8 {project_path}/deploy/deploy.py receive_workspace
python3.8 {project_path}/deploy/deploy.py release_workspace
sleep 3
nohup python3.8 {project_path}/startproject/reboot_phone.py >/dev/null 2>&1 &
sleep 120
if [ -d "{project_path}/workspaces/Process" ]; then
    rm -rf {project_path}/workspaces/Process
fi

echo "============================== Linux deploy end ! =============================="
echo "****************************** Start youwant project . ******************************"

cd {project_path}/workspaces/device1
bash {project_path}/workspaces/device1/device1.sh
echo "comment1 start OK ! "

sleep 60
echo "*/5 * * * * . /etc/profile;cd {project_path}/workspaces/monitor && python3.8 {project_path}/workspaces/monitor/monitor.py &" >> /var/spool/cron/root
echo "****************************** Start youwant project OK ! ******************************"
echo "============================== All steps completed ! =============================="
"""


def read_conf(config_path):
    """
    读取监控配置文件
    :param config_path:配置文件路径
    :return:配置文件
    """
    config = None
    try:
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
    except Exception as e:
        print("Project is not run .")
    return config


def create_shell(start_sh, project_path):
    """
    创建项目启动文件
    :param start_sh: 项目启动sh文件
    :param project_path: 项目目录
    :return:
    """
    with open(start_sh, mode="w", encoding="utf-8") as f:
        f.write(cmd_str.format(project_path=project_path))


if __name__ == '__main__':
    project_path = read_conf("../deploy/build.ini")["project"]["path"]
    start_sh = os.path.join(os.path.join(project_path, "startproject"), "start_project.sh")
    create_shell(start_sh, project_path)
