# -*- coding:utf-8 -*-
# author:xuqien
# data:2020/1/19
"""
安装软件---35
1·定义一个列表(myconf_list)和字典(myconf_dict)存储经常没有安装上去的软件和文件信息，方便后期修改和维护
2·用列表把报错内容和安装文档直接匹配关联
3·用列表把报错内容匹配，再把符合的字符串当作字典的Key取得字典中的值
4·把列表直接匹配成功的和字典取值成功的标记保存起来
5·再把被标记保存的字符串与爬取到的安装文档内容进行检索匹配，获取安装文档的头部信息，保存
6·把保存的字符串进行切片、正则、拼接得到装机指令字符串
7·用队列或者进程池实现装机
"""

from urllib.request import urlopen
import threading
import time
import urllib
import os
import re
from queue import Queue


def get_file_msg():
    global res, file
    data_list = list()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    url = input("请输入安装文档URL地址:").strip()
    try:
        req = urllib.request.Request(url,headers=headers)
        res = urlopen(req)
    except:
        print("无法获得文档请求。请检查网络是否可达!")
    data = res.read().decode("gbk")
    # print(type(data))
    with open("data.py", 'w') as f:
        if data:
            f.write(data)
    try:
        file = open("./data.py", 'r')
    except:
        print("打开爬取内容的文件失败!")
    else:
        while True:
            data = file.readline()
            if not data:
                break
            else:
                re_data_list = re.findall(r"<font color=red>.*</font>", data)
                if len(re_data_list) > 0:
                    # print(re_data_list)
                    re_data_list_new = re.sub(r"<[\w \=\/]*>", "", re_data_list[0])
                    re_data_list_new2 = re.split(r"[()]", re_data_list_new)
                    if len(re_data_list_new) > 8:
                        temp = 0
                        for item in re_data_list_new2:
                            temp += 1
                            if len(item) < 1:
                                re_data_list_new2.pop(temp - 1)
                        data_list.append(re_data_list_new2)
        if os.path.exists("./data.py"):
            os.system("rm data.py")
    finally:
        file.close()
    return data_list


def get_err_msg():
    stopword = ":q"
    err_msg = ""
    print("请输入错误信息，[:q]结束输入:")
    for line in iter(input, stopword):
        err_msg = err_msg + line
    return err_msg


def get_myconf_file():
    with open("./myconf_list.py", 'r') as fl:
        content_list = fl.read()
    with open("./myconf_dict.py", 'r') as fd:
        content_dict = fd.read()
    # print(content_list,content_dict)
    myconf_list = eval(content_list)
    myconf_dict = eval(content_dict)
    return myconf_list,myconf_dict


def search_errkeywords(err_msg_str, conf_msg_list, conf_msg_dict):
    err_list = list()
    for item in conf_msg_list:
        try:
            get_err = re.search(item, err_msg_str)
            ret = get_err.group()
            # print(ret)
        except:
            continue
        else:
            err_list.append(ret)
    for item in err_list:
        try:
            dict_value = conf_msg_dict[item]
        except:
            continue
        else:
            err_list.remove(item)
            err_list.append(dict_value)  
    return err_list


def get_installmsg(err_list, file_list):
    install_list = list()
    for item_list in file_list:
        flag = False
        for item in item_list:
            for goal in err_list:
                try:
                    re.search(goal, item, re.IGNORECASE).group()
                except:
                    continue
                else:
                    if flag == False:
                        install_list.append(item_list)
                    flag = True
    return install_list


def get_machine_msg():
    global ip_str, mac_str
    temp_str = input("请输入机器信息:").strip()
    if len(temp_str.split(",")) == 5 and re.search(r"[0-9]", temp_str[:1]):
        temp_list = temp_str.split(",")
        ip_str = temp_list[0]
        mac_str = temp_list[1]
    return [ip_str, mac_str]


#def ready_queue(queue,comm_list):
    #for item in comm_list:
        #queue.put(item)
    #time.sleep(2)


def begin_install(queue):
        os.system(queue.get())


def implement_install(install_list, ip_str, mac_str):
    str_install = list()
    str_check = list()
    comm_list = list()
    for item_list in install_list:
        if len(item_list) < 5:
            continue
        str_install.append(item_list[1].split(":")[1])
        str_check.append(item_list[3].split(":")[1])
    # print(str_install, str_check)
    i = 0
    while True:
        if i >= len(str_install):
            break
        # print(i)
        temp_str = " autosetup.sh -i " + str_install[i] + " -c " + str_check[i] + " -h " + ip_str + " -n " + mac_str
        # print(temp_str)
        comm_list.append(temp_str)
        i += 1
    # print(comm_list)
    q = Queue(len(comm_list))
    for item in comm_list:
        q.put(item)
    time.sleep(2)
    while True:
        t = threading.Thread(target=begin_install, args=(q,))
        t.start()
        if q.empty() == True:
            break


def main():
    # 获取错误的信息
    err_msg_str = get_err_msg()
    # print(err_msg_str)
    # 获取线上的安装文档
    file_msg_list = get_file_msg()
    # print(file_msg_list)
    # 获取错误配置
    conf_msg_list,conf_msg_dict = get_myconf_file()
    # print(conf_msg_list,conf_msg_dict)
    # 用配置文件的信息和错误的信息进行匹配
    err_msg_list = search_errkeywords(err_msg_str, conf_msg_list, conf_msg_dict)
    # print(err_msg_list)
    # 用返回的错误信息列表遍历匹配线上的文档
    install_list = get_installmsg(err_msg_list, file_msg_list)
    # print(install_list)
    # print(len(install_list))
    # 获取机器信息
    ip_str,mac_str = get_machine_msg()
    # print(ip_str,mac_str)
    # 实现自动装机
    implement_install(install_list, ip_str, mac_str)


if __name__ == "__main__":
    try:
        main()
    except Exception as other:
        print("unknown error !")
