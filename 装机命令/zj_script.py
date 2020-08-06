#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:xuqien
# data:2020/1/19

import os


def installscript():
    stopword = ":q"
    str_zjurl = ""
    print("请直接粘贴复制到的文档头【单独输入‘:q‘保存退出】【输入exit()退出脚本】:")
    for line in iter(input, stopword):
        # 对输入的多行内容进行迭代遍历为一行字符串
        str_zjurl = str_zjurl + line
    # print(str_zjurl)
    if str_zjurl == "exit()":
        print("退出脚本！")
        return str_zjurl
    list_str = str_zjurl.split(":")
    # print(list_str)
    if ((list_str[0] == "安装脚本路径") or (list_str[0] == "(安装脚本")) \
            and (list_str.__len__() == 4 or list_str.__len__() == 7):
        if list_str[0] == "安装脚本路径" and list_str.__len__() == 4:
            str_1 = list_str[1][0:list_str[1].__len__()-6]
            # print(str_1)
            str_2 = list_str[3]
            # print(str_2)
        elif list_str[0] == "(安装脚本" and list_str.__len__() == 7:
            str_1 = list_str[1][0:list_str[1].__len__()-8]
            # print(str_3)
            str_2 = list_str[3][0:list_str[3].__len__()-5]
            # print(str_4)
        else:
            print("输入不正确，请复制正确的文档头!")
            return
    else:
        print("输入不正确，请复制正确的文档头!")
        return
    str_zjmachine = input("请粘贴IP和机器名,并按回车键执行装机:")
    if len(str_zjmachine.split(",")) == 5:
        if not (str_zjmachine.startswith("1")
                or str_zjmachine.startswith("2")
                or str_zjmachine.startswith("3")
                or str_zjmachine.startswith("4")
                or str_zjmachine.startswith("5")
                or str_zjmachine.startswith("6")
                or str_zjmachine.startswith("7")
                or str_zjmachine.startswith("8")
                or str_zjmachine.startswith("9")):
            print("输入不正确，请复制正确的主机名和IP!")
            return
        # >2 对输入的主机名和IP进行处理
        list_4 = str_zjmachine.split(",")
        str_3 = list_4[0]
        str_4 = list_4[1]
        # print(str_3)
        # print(str_4)
    else:
        print("输入不正确，请复制正确的主机名和IP!")
        return

    # 2.对处理的字符串结果进行拼接
    result_com = "autosetup.sh " + "-i " + str_1 + " -c " + str_2 + " -h " + str_3 + " -n " + str_4
    # print(result_com)
    os.system(result_com)
    return


if __name__ == '__main__':
    while True:
        str_f = installscript()
        if str_f == "exit()":
            break