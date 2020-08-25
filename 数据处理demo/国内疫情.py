import requests
import json
import time
import pandas
import numpy
from lxml import etree
from matplotlib import pyplot
from matplotlib import font_manager


class Show_COVID_19(object):

    def __init__(self):
        self.url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3"

    def get_net_msg(self):
        print("正在爬取新冠肺炎网络统计数......")
        time.sleep(1)
        resp = requests.get(self.url)
        content = resp.content.decode("unicode_escape")
        # print(content)
        ret = etree.HTML(content)
        info_msg_list = ret.xpath("//script[@id='captain-config']/text()")
        print("爬取数据成功！")
        # print(info_msg_list)
        time.sleep(1)
        return info_msg_list

    def deal_msg(self,info_msg_list):
        print("正在处理数据......")
        time.sleep(1)
        domestic_info = dict()
        for i in info_msg_list:
            info_msg_dict = json.loads(i, strict=False)
            # print(info_msg_dict["component"][0]["trend"])
            domestic_info["日期"] = info_msg_dict["component"][0]["trend"]["updateDate"]
            domestic_info["确诊"] = info_msg_dict["component"][0]["trend"]["list"][0]["data"]
            domestic_info["疑似"] = info_msg_dict["component"][0]["trend"]["list"][1]["data"]
            domestic_info["治愈"] = info_msg_dict["component"][0]["trend"]["list"][2]["data"]
            domestic_info["死亡"] = info_msg_dict["component"][0]["trend"]["list"][3]["data"]
            domestic_info["新增确诊"] = info_msg_dict["component"][0]["trend"]["list"][4]["data"]
            domestic_info["新增疑似"] = info_msg_dict["component"][0]["trend"]["list"][5]["data"]
            domestic_info["新增治愈"] = info_msg_dict["component"][0]["trend"]["list"][6]["data"]
            domestic_info["新增死亡"] = info_msg_dict["component"][0]["trend"]["list"][7]["data"]
            domestic_info["新增境外输入"] = info_msg_dict["component"][0]["trend"]["list"][8]["data"]
        return domestic_info

    def info_msg(self,domestic_info):
        temp_len = len(domestic_info["日期"])
        for i in range(temp_len):
            temp_dict = dict()
            temp_dict["日期"] = domestic_info["日期"][i]
            temp_dict["确诊"] = domestic_info["确诊"][i]
            temp_dict["疑似"] = domestic_info["疑似"][i]
            temp_dict["治愈"] = domestic_info["治愈"][i]
            temp_dict["死亡"] = domestic_info["死亡"][i]
            temp_dict["新增确诊"] = domestic_info["新增确诊"][i]
            temp_dict["新增疑似"] = domestic_info["新增疑似"][i]
            temp_dict["新增治愈"] = domestic_info["新增治愈"][i]
            temp_dict["新增死亡"] = domestic_info["新增死亡"][i]
            temp_dict["新增境外输入"] = domestic_info["新增境外输入"][i]
            print(temp_dict)
            time.sleep(0.2)
        print("数据处理完成！")
        time.sleep(1)

    def draw(self,domestic_info):
        print("开始绘制折现图......")
        time.sleep(1)
        my_font = font_manager.FontProperties(fname=r'C:\WINDOWS\Fonts\simhei.ttf', size=12)
        pyplot.figure(figsize=(30, 14), dpi=80)
        x = domestic_info["日期"]
        y_1 = domestic_info["确诊"]
        y_2 = domestic_info["疑似"]
        y_3 = domestic_info["治愈"]
        y_4 = domestic_info["死亡"]
        y_5 = domestic_info["新增确诊"]
        y_6 = domestic_info["新增疑似"]
        y_7 = domestic_info["新增治愈"]
        y_8 = domestic_info["新增死亡"]
        y_9 = domestic_info["新增境外输入"]
        pyplot.plot(range(len(x)), y_1, label="确诊")
        # print(len(y_1),len(x),len(y_2),len(y_3),len(y_4),len(y_5),len(y_6),len(y_7),len(y_8),len(y_9))
        pyplot.plot(range(len(x)), y_2, label="疑似")
        pyplot.plot(range(len(x)), y_3, label="治愈")
        pyplot.plot(range(len(x)), y_4, label="死亡")
        pyplot.plot(range(len(x)), y_5, label="新增确诊")
        pyplot.plot(range(len(x)), y_6, label="新增疑似")
        pyplot.plot(range(len(x)), y_7, label="新增治愈")
        pyplot.plot(range(len(x)), y_8, label="新增死亡")
        pyplot.plot(range(len(x)), y_9, label="新增境外输入")
        pyplot.legend(prop=my_font)
        pyplot.xlabel("日期", fontproperties=my_font)
        pyplot.ylabel("人数", fontproperties=my_font)
        pyplot.title("国内疫情详情变化图", fontproperties=my_font)
        pyplot.xticks(range(len(x)), x)
        print("绘制完成,准备展示，并保存到本地！")
        pyplot.savefig("./world.png")
        time.sleep(1)
        print("已保存为world.png")
        pyplot.show()

    def run(self):
        # 获取信息
        info_msg_list = self.get_net_msg()
        # 信息处理
        domestic_info = self.deal_msg(info_msg_list)
        # 打印信息
        self.info_msg(domestic_info)
        # 绘制折线图
        self.draw(domestic_info)


if __name__ == '__main__':
    sc_19 = Show_COVID_19()
    sc_19.run()