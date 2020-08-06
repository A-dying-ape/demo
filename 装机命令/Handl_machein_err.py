# -*- coding:utf-8 -*-
# author:xuqien
# data:2020/1/19
"""
功能不全面，只解决一些常遇到的问题
"""

import os
import sys
import time
import re
import extent_method


def yum_geoip(err_info):
    if re.search(r"GeoIP", err_info, re.IGNORECASE):
        os.system("yum -y install GeoIP")


def handl_dns(err_info):
    if re.search(r"sdn service is stop", err_info):
        os.system("killall -9 sdn > xqe_txt_2")
        os.system("ifconfig lo up > xqe_txt_1")
        os.system("rm -rf xqe_txt_*")
    elif re.search(r"ts_dns@chinanetcenter.com", err_info):
        os.system("chattr -i /etc/resolv.conf")
        os.system("perl /usr/local/bin/nsping.sh")


def handl_lvs_err(err_info):
    if re.search(r"rpm -e ldirectord", err_info):
        flag = os.path.exists("/etc/ha.d/ldirectord.cf")
        if flag == False:
            print("缺少/etc/ha.d/ldirectord.cf文件无法卸载ldirectord，拷贝!")
        else:
            os.system("service ospf_switch restart > xqe_txt_1")
            os.system("rpm -e ldirectord > xqe_txt_2")
            with open("xqe_txt_2","r") as f:
                content = f.read()
            if re.search(r"nicGroOff.sh", content):
                print("缺少/etc/ha.d/haresources文件无法卸载ldirectord，拷贝!")
            else:
                os.system("rpm -e ldirectord > xqe_txt_3")
        os.system("rm -rf xqe_txt_*")
    elif re.search(r"ERROR: The IP.*Department!", err_info):
        print("IP信息配置到其他网卡上面,请找设备组修改网卡配置!")
    elif re.search(r"crontab not configured", err_info):
        os.system("crontab -e")
    elif re.search(r"check numa failed, see details in fw_log", err_info):
        print("问题收集中，未处理。。。")


def handl_disk_journal(err_info):
    if re.search(r"Disk.*notok",err_info):
        extent_method.run()


# def check_shark(err_info):
    # if re.search(r"shark.pid", err_info):
        # os.system("touch /usr/local/shark/var/run/shark.pid")
    # os.system("chattr -i /usr/local/shark/etc/shark.conf > xqe_txt_1")
    # os.system("service shark restart > xqe_txt_2")
    # os.system("rm -rf xqe_txt_*")


def handl_wsxserver(err_info):
    if re.search(r"ERROR:.*wsxserver", err_info):
        port = re.search(r"Port.? (\d*) .?No .?Listened .?by .?wsxserver", err_info).group(1)
        comm_one = "netstat -anp |grep %s |awk '{print $7}' > xqe_txt_1" % port
        os.system(comm_one)
        app_list = list()
        file = open("xqe_txt_1", "r")
        while True:
            if not file.readline():
                break
            temp_str = file.readline().strip("").split("/")
            if len(temp_str) == 2:
                app_list.append(temp_str[1].strip())
        file.close()
        load_app = list(set(app_list))
        for item in load_app:
            restart_comm = "service %s restart" % item
            os.system(restart_comm)
        os.system("service wsxserver restart > xqe_txt_2")
        os.system("rm -rf xqe_txt_*")


def get_cache_swap():
    os.system("df |grep cache|awk '{print $2}' > xqe_txt_1")
    temp_list_1 = list()
    temp_list_2 = list()
    f = open("xqe_txt_1","r")
    while True:
        con = f.readline()
        content = con[0:len(con)-1]
        if not con:
            break
        temp_list_1.append(content)
    f.close()
    min_len = min([(len(x)) for x in temp_list_1])
    for item in temp_list_1:
        if len(item) == min_len:
            temp_list_2.append(item)
    temp_list_3 = list(set(temp_list_2))
    for item in temp_list_3:
        comm_one = "df |grep cache |grep %s|awk '{print $1,$6}' >> xqe_txt_2" % item
        os.system(comm_one)
    with open("xqe_txt_2", "r") as f:
        content = f.read()
    temp_list_4 = re.split(r" |\n", content)
    temp_list_4.pop(len(temp_list_4)-1)
    for item in temp_list_4:
        if re.search(r"cache", item):
            os.system("fuser -m -k %s" % item)
            os.system("umount %s" % item)
    temp_num = len(temp_list_4)
    while True:
        os.system("mkfs.ext4 -i 4096 -L %s %s" %(temp_list_4[temp_num - 1], temp_list_4[temp_num - 2]))
        temp_num -= 2
        if temp_num <= 0:
            break
    os.system("mount -a")
    os.system("rm xqe_txt_*")


def check_ssd(err_info):
    err_str_one = "wrong SSD_inode"
    err_str_two = "SSD_noUse"
    err_str_three = "SSD_mount_point"
    if re.search(err_str_three, err_info):
        print("磁盘挂载与平台不一致!")
        os.system("df -h|grep cache")
        sys.exit(0)
    elif re.search(err_str_two, err_info):
        get_cache_swap()
    elif re.search(err_str_one, err_info):
        get_cache_swap()


def check_cs_status(err_info):
    err_str_one = "SSD"
    err_str_two = "cache_dir"
    err_str_three = "squid.conf"
    err_str_four = "initLogCollect Failure!"
    err_str_five = "measured"
    if re.search(err_str_one, err_info):
        extent_method.run()
    elif re.search(err_str_two, err_info):
        extent_method.run()
    elif re.search(err_str_three, err_info):
        extent_method.run()
    elif re.search(err_str_four, err_info):
        extent_method.run()
        print("当前squid版本信息:")
        os.system("cat /usr/local/squid/etc/squid.conf | grep CNC_CDN_CONF_VERSION")
    elif re.search(err_str_five, err_info):
        extent_method.run()


def white_list_check(err_info):
    common_one = "service shark restart > xqe_txt_1;"
    if re.search(r".*white_lis.*", err_info):
        print("白名单部署失败，请返回部署！")
    else:
        os.system(common_one)
        with open("xqe_txt_1", "r") as f:
            content = f.read()
        try:
            re.search(r"events", content).group()
        except:
            return
        print("白名单部署失败，请返回部署！")
    os.system("rm -rf xqe_txt_*")


def judge_kernel(err_info):
    eflag = os.path.exists("/etc/grub.conf")
    if eflag == False:
        print("/etc/grub.conf文件不存在!内核异常！")
        print("grub.conf详解: https://blog.51cto.com/zz6547/1852788")
        print("grub.conf配置: https://www.cnblogs.com/zwl715/p/3627953.html")
        sys.exit(0)
    bflag = os.path.exists("/boot/grub/grub.conf")
    if bflag == False:
        print("/boot/grub/grub.conf文件不存在!内核异常！")
        print("grub.conf详解: https://blog.51cto.com/zz6547/1852788")
        print("grub.conf配置: https://www.cnblogs.com/zwl715/p/3627953.html")
        sys.exit(0)
    if re.search(r"WARN:.*kernel effective!", err_info):
        ver = re.search(r"WARN: please reboot to make \"(.*)\" kernel effective!", err_info).group(1)
        os.system("cat /boot/grub/grub.conf > xqe_txt_4")
        with open("xqe_txt_4", "r") as f:
            kernel_info = f.read()
        try:
            re.search(ver, kernel_info).group()
        except:
            print("缺少内核启动项!")
            os.system("rm -rf xqe_txt_*")
            sys.exit(0)
    try:
        re.search(r"WARN:.*kernel effective!", err_info).group()
    except:
        print("内核正常!")
        os.system("rm -rf xqe_txt_*")
        return
    else:
        comm_one = "last reboot -a > xqe_txt_1;head -n 1 xqe_txt_1"
        temp_file_1 = os.popen(comm_one)
        last_reboot = temp_file_1.read()
        print("最后的重启机器信息:"+last_reboot.strip())
        comm_two = "last reboot -a > xqe_txt_1;head -n 2 xqe_txt_1 > xqe_txt_2;tail -n 1 xqe_txt_2|awk '{print $4,$5,$6,$9}'"
        temp_file_2 = os.popen(comm_two)
        t1 = temp_file_2.read()
        last_t = time.mktime(time.strptime(t1.strip(), "%a %b %d %H:%M"))
        comm_three = "last reboot -a > xqe_txt_3;head -n 1 xqe_txt_3|awk '{print $4,$5,$6,$7}'"
        temp_file_3 = os.popen(comm_three)
        t2 = temp_file_3.read()
        near_t = time.mktime(time.strptime(t2.strip(), "%a %b %d %H:%M"))
        daytime = (near_t - last_t)/3600/24
        print("距离上一次重启的时间为:%.2f" % daytime)
        os.system("rm -rf xqe_txt_*")
        if daytime > 1:
            os.system("reboot")
        else:
            print("请确定是否重启机器？")


def judge_common():
    try:
        tools_common_res = sys.argv[1]
    except:
        pass
    else:
        rm_comm = "xqe_txt_*"
        # comm_one = "cd /usr/local/src/;ls -l -h|grep tools-common-res-|awk '{print $9}' > xqe_txt_1;head -n 1 xqe_txt_1"
        # temp_file_1 = os.popen(comm_one)
        # tools_common_res = temp_file_1.read()
        # with open("tools_common_res_version.py", "r") as f:
            #tools_common_res = f.readline()
        flag = os.path.exists("/usr/local/src/"+tools_common_res.strip())
        if flag == False:
            print("没有公共包的软件包和文件，请尝试手动下载!")
            os.system('rm -rf /usr/local/src/'+rm_comm)
            sys.exit(0)
        os.system('rm -rf /usr/local/src/'+rm_comm)

        temp_file_2 = os.popen('rpm -qa | wc -l')
        ret = temp_file_2.read()
        rpmpackage_num = int(ret)
        if rpmpackage_num < 600:
            print("RPM数据库异常，请重新安装系统!")
            sys.exit(0)

        comm_three = "cd /usr/local/src;ls -l -h|grep % s|awk  '{print $5}' > xqe_txt_3;tail -n 1 xqe_txt_3" % tools_common_res
        temp_file_3 = os.popen(comm_three)
        common_size = temp_file_3.read()
        if not common_size.startswith("7"):
            print("公共包大小异常！可能是网络问题！")
        os.system("rm -rf /usr/local/src/"+rm_comm)

        comm_two = "rm -rf /var/lib/rpm/__db.00*;rpm --rebuilddb"
        os.system(comm_two)
        print("检测机器连通性，看看是否IP和端口被封!")
        os.system("ping -c5 -i1 www.baidu.com > xqe_txt_5")
        count=len(open(r"xqe_txt_5",'rU').readlines()) 
        if count < 10:
            print("网络异常，请找网络组排查!")
        os.system("/usr/local/scmagent/doctor/doctor-S ")
        print("*"*30+"检测完毕！"+"*"*30)

        comm_four = "sh /usr/local/src/"+tools_common_res.strip()+"/wsComm_Check.sh > xqe_txt_4;tail -n 1 xqe_txt_4"
        temp_file_4 = os.popen(comm_four)
        common_err_msg = temp_file_4.read()
        if len(common_err_msg) != 1:
            print("ERR:"+common_err_msg)
            print("请手动安装缺少的组件!")
            return
        else:
            print("公共包正常!")
        os.system("rm -rf "+rm_comm)


def get_err_info():
    err_filename = input("请输入检测脚本名称用引号括起来:").strip()
    if re.match(r"(.*\.sh$)", err_filename):
        temp_comm = "sh /usr/local/src/"+err_filename+" > err_info"
    else:
        temp_comm = "sh /usr/local/src/"+err_filename+".sh > err_info"
    os.system(temp_comm)
    with open("./err_info", 'r') as f:
        err_info = f.read()
    return err_info


def main():
    # 1.错误重定向
    err_info = get_err_info()
    # 2.判断公共包是否有安装
	# try:
    judge_common()
	# except:
		# pass
    # 3.内核检测
    judge_kernel(err_info)
    # 4.检测是否白名单
    white_list_check(err_info)
	# 5.检测固盘
    check_ssd(err_info)
    # 6.检测cache，squid
    check_cs_status(err_info)
    # 7.wsxserver检测
    handl_wsxserver(err_info)
    # 8.检测shark服务
    # check_shark(err_info)
    # 9.LVS相关
    handl_lvs_err(err_info)
    # 10.DNS相关
    handl_dns(err_info)
    # 11.GeoIP
    yum_geoip(err_info)

if __name__ == "__main__":
    try:
        main()
    except:
        print("unknown error !")