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
cd {project_path}/startproject
python3.8 /wechatserver/wxhook/startproject/kill_process.py
cd {project_path}/deploy
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
cd {project_path}/workspaces/comment1
bash {project_path}/workspaces/comment1/comment1.sh
echo "comment1 start OK ! "

cd {project_path}/workspaces/comment2
bash {project_path}/workspaces/comment2/comment2.sh
echo "comment2 start OK ! "

cd {project_path}/workspaces/comment3
bash {project_path}/workspaces/comment3/comment3.sh
echo "comment3 start OK ! "

cd {project_path}/workspaces/detail1
bash {project_path}/workspaces/detail1/detail1.sh
echo "detail1 start OK ! "

cd {project_path}/workspaces/detail2
bash {project_path}/workspaces/detail2/detail2.sh
echo "detail2 start OK ! "

cd {project_path}/workspaces/detail3
bash {project_path}/workspaces/detail3/detail3.sh
echo "detail3 start OK ! "

cd {project_path}/workspaces/detail4
bash {project_path}/workspaces/detail4/detail4.sh
echo "detail4 start OK ! "

cd {project_path}/workspaces/detail5
bash {project_path}/workspaces/detail5/detail5.sh
echo "detail5 start OK ! "

cd {project_path}/workspaces/detail6
bash {project_path}/workspaces/detail6/detail6.sh
echo "detail6 start OK ! "

cd {project_path}/workspaces/detail7
bash {project_path}/workspaces/detail7/detail7.sh
echo "detail7 start OK ! "

cd {project_path}/workspaces/detail8
bash {project_path}/workspaces/detail8/detail8.sh
echo "detail8 start OK ! "

cd {project_path}/workspaces/detail9
bash {project_path}/workspaces/detail9/detail9.sh
echo "detail9 start OK ! "

cd {project_path}/workspaces/detail10
bash {project_path}/workspaces/detail10/detail10.sh
echo "detail10 start OK ! "

cd {project_path}/workspaces/detail11
bash {project_path}/workspaces/detail11/detail11.sh
echo "detail11 start OK ! "

# cd {project_path}/workspaces/detail12
# bash {project_path}/workspaces/detail12/detail12.sh
# echo "detail12 start OK ! "

cd {project_path}/workspaces/livesquare1
bash {project_path}/workspaces/livesquare1/livesquare1.sh
echo "livesquare1 start OK ! "

cd {project_path}/workspaces/livesquare2
bash {project_path}/workspaces/livesquare2/livesquare2.sh
echo "livesquare2 start OK ! "

cd {project_path}/workspaces/product1
bash {project_path}/workspaces/product1/product1.sh
echo "product1 start OK ! "

cd {project_path}/workspaces/product2
bash {project_path}/workspaces/product2/product2.sh
echo "product2 start OK ! "

cd {project_path}/workspaces/product3
bash {project_path}/workspaces/product3/product3.sh
echo "product3 start OK ! "

cd {project_path}/workspaces/product4
bash {project_path}/workspaces/product4/product4.sh
echo "product4 start OK ! "

cd {project_path}/workspaces/product5
bash {project_path}/workspaces/product5/product5.sh
echo "product5start OK ! "

cd {project_path}/workspaces/product6
bash {project_path}/workspaces/product6/product6.sh
echo "product6 start OK ! "

cd {project_path}/workspaces/product7
bash {project_path}/workspaces/product7/product7.sh
echo "product7 start OK ! "

cd {project_path}/workspaces/product8
bash {project_path}/workspaces/product8/product8.sh
echo "product8 start OK ! "

cd {project_path}/workspaces/product9
bash {project_path}/workspaces/product9/product9.sh
echo "product9 start OK ! "

cd {project_path}/workspaces/product10
bash {project_path}/workspaces/product10/product10.sh
echo "product10 start OK ! "

cd {project_path}/workspaces/product11
bash {project_path}/workspaces/product11/product11.sh
echo "product11 start OK ! "

cd {project_path}/workspaces/product12
bash {project_path}/workspaces/product12/product12.sh
echo "product12 start OK ! "

cd {project_path}/workspaces/product13
bash {project_path}/workspaces/product13/product13.sh
echo "product13 start OK ! "

cd {project_path}/workspaces/product14
bash {project_path}/workspaces/product14/product14.sh
echo "product14 start OK ! "

cd {project_path}/workspaces/product15
bash {project_path}/workspaces/product15/product15.sh
echo "product15 start OK ! "

cd {project_path}/workspaces/topic1
bash {project_path}/workspaces/topic1/topic1.sh
echo "topic1 start OK ! "

cd {project_path}/workspaces/topic2
bash {project_path}/workspaces/topic2/topic2.sh
echo "topic2 start OK ! "

cd {project_path}/workspaces/livemsg1
bash {project_path}/workspaces/livemsg1/livemsg1.sh
echo "livemsg1 start OK ! "

cd {project_path}/workspaces/livemsg2
bash {project_path}/workspaces/livemsg2/livemsg2.sh
echo "livemsg2 start OK ! "

cd {project_path}/workspaces/livemsg3
bash {project_path}/workspaces/livemsg3/livemsg3.sh
echo "livemsg3 start OK ! "

cd {project_path}/workspaces/livemsg4
bash {project_path}/workspaces/livemsg4/livemsg4.sh
echo "livemsg4 start OK ! "

cd {project_path}/workspaces/livemsg5
bash {project_path}/workspaces/livemsg5/livemsg5.sh
echo "livemsg5 start OK ! "

cd {project_path}/workspaces/liveonline1
bash {project_path}/workspaces/liveonline1/liveonline1.sh
echo "liveonline1 start OK ! "

cd {project_path}/workspaces/liveonline2
bash {project_path}/workspaces/liveonline2/liveonline2.sh
echo "liveonline2 start OK ! "

cd {project_path}/workspaces/liveonline3
bash {project_path}/workspaces/liveonline3/liveonline3.sh
echo "liveonline3 start OK ! "

cd {project_path}/workspaces/liveproduct1
bash {project_path}/workspaces/liveproduct1/liveproduct1.sh
echo "liveproduct1 start OK ! "

cd {project_path}/workspaces/liveproduct2
bash {project_path}/workspaces/liveproduct2/liveproduct2.sh
echo "liveproduct2 start OK ! "

cd {project_path}/workspaces/liveproduct3
bash {project_path}/workspaces/liveproduct3/liveproduct3.sh
echo "liveproduct3 start OK ! "

cd {project_path}/workspaces/liveproduct4
bash {project_path}/workspaces/liveproduct4/liveproduct4.sh
echo "liveproduct4 start OK ! "

cd {project_path}/workspaces/livedanmu1
bash {project_path}/workspaces/livedanmu1/livedanmu1.sh
echo "livedanmu1 start OK ! "

# cd {project_path}/workspaces/livedanmu2
# bash {project_path}/workspaces/livedanmu2/livedanmu2.sh
# echo "livedanmu2 start OK ! "

# cd {project_path}/workspaces/livedanmu3
# bash {project_path}/workspaces/livedanmu3/livedanmu3.sh
# echo "livedanmu3 start OK ! "

cd {project_path}/workspaces/videoproduct1
bash {project_path}/workspaces/videoproduct1/videoproduct1.sh
echo "videoproduct1 start OK ! "

cd {project_path}/workspaces/videoproduct2
bash {project_path}/workspaces/videoproduct2/videoproduct2.sh
echo "videoproduct2 start OK ! "

cd {project_path}/workspaces/videourl1
bash {project_path}/workspaces/videourl1/videourl1.sh
echo "videourl1 start OK ! "

cd {project_path}/workspaces/hourlist1
bash {project_path}/workspaces/hourlist1/hourlist1.sh
echo "hourlistl1 start OK ! "

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
