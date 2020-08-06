import os
import zj_logo


def create_zj():
    # 1.对输入的内容进行处理
    zj_logo.zj_menu()
    stopword = ":q"
    str_zjurl = ""
    print("请直接粘贴复制到的文档头【单独输入‘:q‘保存退出】:")
    for line in iter(input, stopword):
        # 对输入的多行内容进行迭代遍历为一行字符串
        str_zjurl = str_zjurl + line
    if not ((str_zjurl.startswith("(安装脚本:") and str_zjurl.endswith(")")) or str_zjurl.startswith("")):
        print("输入不正确，请复制正确的文档头!")
        return
    else:
        if str_zjurl.startswith("(安装脚本:") and str_zjurl.endswith(")"):
            # >1 对输入的文档头进行处理
            list_1 = str_zjurl.split(")(")
            list_2 = list_1[0].split(":")
            list_3 = list_1[2].split(":")
            str_1 = list_2[1]
            str_2 = list_3[1]
        elif str_zjurl.startswith(""):
            list_str = str_zjurl.split(":")
            list_str1 = list_str[1][0:-6]
            list_str2 = list_str[3]

    str_zjmachine = input("请直接粘贴复制到的主机名和IP:")
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
        elif not str_zjmachine.split(",")[4][-4:].isalpha():
            print("输入不正确，请复制正确的主机名和IP!")
            return
        else:
            # >2 对输入的主机名和IP进行处理
            list_4 = str_zjmachine.split(",")
            str_3 = list_4[0]
            str_4 = list_4[1]
    else:
        print("输入不正确，请复制正确的主机名和IP!")
        return

    # 2.对处理的字符串结果进行拼接
    result_com = "autosetup.sh " + "-i" + str_1 + " -c " + str_2 + " -h " + str_3 + " -n " + str_4
    print(result_com)
    # os.system(result_com)
    return


def create_kb():
    # 1.提示用户操作
    zj_logo.kb_menu()
    return