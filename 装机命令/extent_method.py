# -*- coding:utf-8 -*-
# author:xuqien
# data:2020/1/19

import os
import re
import datetime
import time
import sys


def stepone():
    str_rmf = "mv /usr/local/squid/etc/squid.conf /tmp/"
    str_cur = "/bin/cp /usr/local/scmagent/backup/config-deploy/current/squid*  /usr/local/squid/etc/ > txt"
    str_etc = "/usr/local/squid/etc/squid.conf"
    check_common = "/usr/local/squid/etc/squid-common.conf"

    """查看130流水是否有生成文件squid.conf"""
    os.system(str_rmf)
    size = os.path.exists("/usr/local/scmagent/backup/config-deploy/current/squid.conf")
    if size == False:
        print("请走130流水部署下配置！")
        sys.exit(0)
    os.system(str_cur)

    """查看squid文件是不是拷贝过来，并且是最新版本"""
    file_one_etc = open(str_etc, 'r')
    while True:
        content_one_etc = file_one_etc.readline()
        if not content_one_etc:
            break
        elif content_one_etc:
            list_con = re.split('[: \n]', content_one_etc)
            for str_l in list_con:
                if str_l == "Date":
                    list_ind = list_con.index(str_l) + 1
                    if (list_ind + 3) <= list_con.__len__()-1:
                        str_f = list_con[list_ind] + " " + list_con[list_ind+1] + ":" + list_con[list_ind+2] + ":" + list_con[list_ind+3]
                        curr_time = datetime.datetime.now()
                        scurr_time = datetime.datetime.strftime(curr_time, "%Y-%m-%d %H:%M:%S")
                        timeend = datetime.datetime.strptime(scurr_time, "%Y-%m-%d %H:%M:%S")
                        timestart = datetime.datetime.strptime(str_f, "%Y-%m-%d %H:%M:%S")
                        t1 = time.mktime(timestart.timetuple()) * 1000 + timestart.microsecond / 1000
                        t2 = time.mktime(timeend.timetuple()) * 1000 + timeend.microsecond / 1000
                        temp_time = t2 - t1
                        day = temp_time/1000/3600/24
                        print("squid.conf文件是%.2f天之前部署的，请查阅近期文档是否有更新!" % day)
                    else:
                        print("squid.conf文件异常")
    file_one_etc.close()
    flag = os.path.exists(check_common)
    if flag == False:
        print("squid-common.conf文件不存在，分割失败，请到线上手动拷贝!")
        sys.exit(0)

def steptwo():
    """初始化squid服务"""
    comdone = "killall -9 squid >txt"
    comdtwo = "ps aux|grep squid > txt"
    comdthree = "rm -rf /usr/local/squid/var/logs/*"
    comdfour = "grep \'^cache_dir\' /usr/local/squid/etc/squid.conf|awk -F\" \" \'{print \"mkdir -p \"$3\"; chown squid:squid \"$3}\'|sh > txt"
    comdfive = "awk -F\"swap-log=\" \'/^cache_dir/{print $2}\' /usr/local/squid/etc/squid.conf|awk -F\"swap.state\" \'/swap.state/{print \"mkdir -p \"$1}\'|sh"
    comdsix = "sed -nr \'/^cache_dir/s@.*swap-log=(.*/swap-log).*@chown -R squid:squid \\1@p\' /usr/local/squid/etc/squid.conf|sort -u|sh"
    comdseven = "/usr/local/squid/sbin/squid -z"
    comdeight = "service squid start"
    os.system(comdone)
    file_two_txt = open("./txt", 'r')
    while True:
        content_two_txt = file_two_txt.readline()
        if not content_two_txt:
            break
        print("squid服务异常或者机器上没有squid进程(error)！")
        file_two_txt.close()
        os.system("rm txt")
        sys.exit(0)
    file_two_txt.close()
    os.system("rm txt")
    os.system(comdtwo)
    file_two_txts = open("./txt", 'r')
    i = 0
    while True:
        content_two_txts = file_two_txts.readline()
        if not content_two_txts:
            break
        i+=1
    if i > 9:
        print("squid服务并没有杀死,或者服务异常，请进入机器确认!")
        file_two_txts.close()
        os.system("rm txt")
        sys.exit(0)
    file_two_txts.close()
    flag = os.path.exists("./txt")
    if flag == True:
        os.system(comdthree)
        os.system(comdfour)
        os.system(comdfive)
        os.system(comdsix)
        os.system(comdseven)
        os.system(comdeight)
    os.system("rm txt")

def stepthree():
    """其他异常排查"""
    check_squid_server = "sysCheckForSquid.sh > txt"
    get_endline = "cat txt | awk \'END {print}\' > txt_p"
    check_squid_log = "tail -n 15 /usr/local/squid/var/logs/squid_cache.log.0 > txt_c"
    os.system(check_squid_server)
    os.system(get_endline)
    file_three_txt = open("./txt_p", 'r')
    content_three_txtt = file_three_txt.read().split(" ")
    content_three_txt = content_three_txtt[0]
    file_three_txt.close()
    if content_three_txt == "fail":
        os.system(check_squid_log)
        file_three_txtc = open("./txt_c", 'r')
        while True:
            content_three_txtc = file_three_txtc.readline()
            if not content_three_txtc:
                break
            print(content_three_txtc)
        os.system("rm txt_c")
        file_three_txtc.close()
        os.system("rm txt_p")
        os.system("rm txt")
        sys.exit()
    os.system("rm txt_p")
    os.system("rm txt")

def run():
    stepone()
    steptwo()
    stepthree()
    print("squid服务没有异常")