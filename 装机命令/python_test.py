"""
input输入多行内容
"""

# stopword = ":q"
# file_content = ""
# print("请输入内容【单独输入‘:q‘保存退出】：")
# for line in iter(input, stopword):
#     file_content = file_content + line + "\n"
#     print(file_content)

# str_1 = "(安装脚本: /home/install.sh)(安装软件列表: /home/installList)(检测脚本: /home/ngb_dc.check.sh)(养护人: wsGAB)"
# list_1 = str_1.split(")(")
# print(list_1)
# list_2 = list_1[0].split(":")
# list_3 = list_1[2].split(":")
# print(list_2)
# print(list_3)
# str_2 = list_2[1]
# str_3 = list_3[1]
# print(type(str_2))
# print(str_3)
# str_4 = ""
# str_result = "autosetup.sh " + "-r" + str_2 + " -c " + str_3 + " -h " + " -n "
# print(str_result)
#
# str2 = "168.101.23.7,ydgdfs104PzsdF105,dwqfeqfqefqwrqw,dqw342,dsaq_w_gFfgaaa"
# print(len(str2.split(",")))
# if not (str2.startswith("1")
#         or str2.startswith("2")
#         or str2.startswith("3")
#         or str2.startswith("4")
#         or str2.startswith("5")
#         or str2.startswith("6")
#         or str2.startswith("7")
#         or str2.startswith("8")
#         or str2.startswith("9")):
#     print("输入不正确，请复制正确的主机名和IP!")
# elif not str2.split(",")[4][-4:].isalpha():
#     print("输入不正确，请复制正确的主机名和IP!")
# else:
#     print("输入正确！")
#
# str1 = "168.101.23.7,ydgdfs104PzsdF105,dwqfeqfqefqwrqw,dqw342,dsaq_w_gFfgaa_a"
# print(str1.split(",")[4][-4:])
# print(str1.split(",")[4][-4:].isalpha())

# str_zjmachine = input("请直接粘贴复制到的主机名和IP:")
# if len(str_zjmachine.split(",")) == 5:
#     if not (str_zjmachine.startswith("1")
#             or str_zjmachine.startswith("2")
#             or str_zjmachine.startswith("3")
#             or str_zjmachine.startswith("4")
#             or str_zjmachine.startswith("5")
#             or str_zjmachine.startswith("6")
#             or str_zjmachine.startswith("7")
#             or str_zjmachine.startswith("8")
#             or str_zjmachine.startswith("9")):
#         print("输入不正确，请复制正确的主机名和IP!")
#     elif not str_zjmachine.split(",")[4][-4:].isalpha():
#         print("输入不正确，请复制正确的主机名和IP!")
#     else:
#         # 2.对处理的字符串结果进行拼接
#         # >2 对输入的主机名和IP进行处理
#         list_4 = str_zjmachine.split(",")
#         str_3 = list_4[0]
#         str_4 = list_4[1]
#         result_com = "autosetup.sh " + "-r" + " -h " + str_3 + " -n " + str_4
#         print(result_com)
# else:
#     print("输入不正确，请复制正确的主机名和IP!")
#
#
# def num_t():
#     num = 10
#     return num
#
#
# num_t()
# stopword = ":q"
# str_zjurl = ""
# print("请直接粘贴复制到的文档头【单独输入‘:q‘保存退出】:")
# for line in iter(input, stopword):
#     # 对输入的多行内容进行迭代遍历为一行字符串
#     str_zjurl = str_zjurl + line
# list_str = str_zjurl.split(":")
# list_str1 = list_str[1][0:-6]
# list_str2 = list_str[3]




# import re
# def pytest():
#     # 1.打开文件
#     str1 = "./123"
#     file = open(str1, 'r', encoding="utf-8")
#     # 2.读取文件的一行，当读取一行后光标会一定到下一行的行首，这样也方便我们行读取所有的文件内容（因为一些文件内容多，我们无法知道）
#     list_return = []
#     while True:
#         text = file.readline()
#         if not text:
#             break
#         elif text:
#             list1 = re.split('[: \n]',text)
#             for str2 in list1:
#                 if str2 == "123":
#                     intc = list1.index(str2) + 1
#                     if intc > list1.__len__() - 1:
#                         index_rang_out = Exception("超出索引！")
#                         raise index_rang_out
#                     else:
#                         str3 = list1[intc]
#                         list_return.append(str3)
#                         print(str3)
#         #     print(list1)
#         # print(text, end="")
#     # 3.关闭文件
#     file.close()
#     return list_return
# try:
#     print(pytest())
# except Exception as index_rang_out:
#     print("%s" % index_rang_out)
# list1 = []
# print(type(list1))
# list1.append("1")
# print(list1[2])
# import os
# file = os.path.getsize("./123")
# if file == 0:
#     print("文件时空的")
# elif file != 0:
#     print("文件不是空的")

# import datetime
# import time
# curr_time = datetime.datetime.now()
# curr_time1 = datetime.datetime.strftime(curr_time, "%Y-%m-%d %H:%M:%S")
# times = "2019-12-01 17:33:33"
# timeend = datetime.datetime.strptime(curr_time1, "%Y-%m-%d %H:%M:%S")
# timestart = datetime.datetime.strptime(times,"%Y-%m-%d %H:%M:%S")
# t1 = time.mktime(timestart.timetuple()) * 1000 + timestart.microsecond / 1000
# t2 = time.mktime(timeend.timetuple()) * 1000 + timeend.microsecond / 1000
# a = t2-t1
# s = a/1000
# m = s/60
# h = m/60
# d = h/24
# print(a,"--",s,"--",m,"--",h,"--",d)

# str1 = "grep /'^cache_dir/' /usr/local/squid/etc/squid.conf|awk -F/" /" /'{print /"mkdir -p /"$3/"; chown squid:squid /"$3}/'|sh"
# str2 = "grep
# comdsix = "sed -nr \'/^cache_dir/s@.*swap-log=(.*/swap-log).*@chown -R squid:squid \\1@p\' /usr/local/squid/etc/squid.conf|sort -u|sh"
# print(comdsix)
# comdfive = "wk -F\"swap-log=\" \'/^cache_dir/{print $2}\' /usr/local/squid/etc/squid.conf|awk -F\"swap.state\" \'/swap.state/{print \"mkdir -p \"$1}\'|sh"
# print(comdfive)

import os
file = open("./123", 'r', encoding="utf-8")
while True:
    text = file.readline()
    if not text:
        break
    if text == "aaa":
        os.system("rm 123")
    print(text)

