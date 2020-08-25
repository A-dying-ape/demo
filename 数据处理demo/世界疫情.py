import requests
import json
import time
from lxml import etree
from pymongo import MongoClient
from matplotlib import pyplot
from matplotlib import font_manager


class World_COVID_19(object):

    def __init__(self):
        self.url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3"
        # 创建mongodb连接
        client = MongoClient(host="127.0.0.1", port=27017)
        self.colection = client["test1"]["world_msg"]

    def get_net_msg(self):
        print("开始爬取数据......")
        time.sleep(1)
        resp = requests.get(self.url)
        content = resp.content.decode("unicode_escape")
        # print(content)
        ret = etree.HTML(content)
        info_msg_list = ret.xpath("//script[@id='captain-config']/text()")
        print("数据抓取完成！")
        time.sleep(1)
        return info_msg_list

    def deal_msg(self,info_msg_list):
        print("开始处理数据......")
        world_info = dict()
        for i in info_msg_list:
            info_msg_dict = json.loads(i, strict=False)
            world_info["累计确诊"] = info_msg_dict["component"][0]["summaryDataOut"]["confirmed"]
            world_info["累计死亡"] = info_msg_dict["component"][0]["summaryDataOut"]["died"]
            world_info["现有确诊"] = info_msg_dict["component"][0]["summaryDataOut"]["curConfirm"]
            world_info["累计治愈"] = info_msg_dict["component"][0]["summaryDataOut"]["cured"]
            world_info["昨日新增累计确诊"] = info_msg_dict["component"][0]["summaryDataOut"]["confirmedRelative"]
            world_info["昨日治愈"] = info_msg_dict["component"][0]["summaryDataOut"]["curedRelative"]
            world_info["昨日死亡"] = info_msg_dict["component"][0]["summaryDataOut"]["diedRelative"]
            world_info["昨日新增现有确诊"] = info_msg_dict["component"][0]["summaryDataOut"]["curConfirmRelative"]
            world_info["更新时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(world_info)
        time.sleep(1)
        print("数据处理完成！")
        return world_info

    def save_2_mongodb(self,world_info):
        time.sleep(1)
        print("将数据保存到Mongodb中......")
        self.colection.insert(world_info)
        time.sleep(1)
        print("已保存到Mongodb！")

    def get_msg_from_mongodb(self):
        time.sleep(1)
        print("正在从Mongodb读取数据")
        world_msg_list = self.colection.find()
        return world_msg_list

    def msg_dismantle(self,world_msg_list):
        print("数据拆解合并中......")
        time.sleep(1)
        temp_list = list()
        for i in world_msg_list:
            temp_dict = dict()
            for k, v in i.items():
                print(k, ":", v)
                temp_dict[k] = v
            temp_list.append(temp_dict)
        time.sleep(1)
        print("拆解合成成功！")
        return temp_list

    def draw_msg1(self,temp_list):
        draw_dict = dict()
        draw_list = list()
        for i in temp_list:
            draw_list.append(i["累计确诊"])
        draw_dict["累计确诊"] = draw_list
        return draw_dict

    def draw_msg2(self,temp_list):
        draw_dict = dict()
        draw_list = list()
        for i in temp_list:
            draw_list.append(i["累计死亡"])
        draw_dict["累计死亡"] = draw_list
        return draw_dict

    def draw_msg3(self,temp_list):
        draw_dict = dict()
        draw_list = list()
        for i in temp_list:
            draw_list.append(i["现有确诊"])
        draw_dict["现有确诊"] = draw_list
        return draw_dict

    def draw_msg4(self,temp_list):
        draw_dict = dict()
        draw_list = list()
        for i in temp_list:
            draw_list.append(i["累计治愈"])
        draw_dict["累计治愈"] = draw_list
        return draw_dict

    def draw_msg5(self,temp_list):
        draw_dict = dict()
        draw_list = list()
        for i in temp_list:
            draw_list.append(i["更新时间"])
        draw_dict["更新时间"] = draw_list
        return draw_dict

    def draw(self,draw_dict1,draw_dict2,draw_dict3,draw_dict4,draw_dict5):
        print("开始绘制世界疫情直方图......")
        time.sleep(1)
        my_font = font_manager.FontProperties(fname=r'C:\WINDOWS\Fonts\simhei.ttf', size=13)
        pyplot.figure(figsize=(30, 14), dpi=80)
        x = draw_dict5["更新时间"]
        y_1 = draw_dict1["累计确诊"]
        y_2 = draw_dict2["累计死亡"]
        y_3 = draw_dict3["现有确诊"]
        y_4 = draw_dict4["累计治愈"]
        pyplot.plot(range(len(x)), y_2, label="累计死亡")
        pyplot.plot(range(len(x)), y_4, label="累计治愈")
        pyplot.plot(range(len(x)), y_3, label="现有确诊")
        pyplot.plot(range(len(x)), y_1, label="累计确诊")
        pyplot.xticks(range(len(x)), x, rotation=90, fontproperties=my_font)
        pyplot.legend(prop=my_font)
        pyplot.ylabel("人数", fontproperties=my_font)
        pyplot.xlabel("日期", fontproperties=my_font)
        pyplot.title("世界疫情详情变化图", fontproperties=my_font)
        pyplot.grid(alpha=0.3)
        print("绘制完成,准备展示，并保存到本地！")
        now_time = str(int(time.time()))
        pyplot.savefig("./world_png/"+now_time)
        time.sleep(1)
        print("已保存为"+"./world_png/"+now_time)
        pyplot.show()

    def run(self):
        # 抓取数据
        info_msg_list = self.get_net_msg()
        # 数据处理
        world_info = self.deal_msg(info_msg_list)
        # 将数据保存到Mongodb
        self.save_2_mongodb(world_info)
        # 从Mongodb读取数据
        world_msg_list = self.get_msg_from_mongodb()
        # 数据拆解合成
        temp_list = self.msg_dismantle(world_msg_list)
        # 准备画图数据
        draw_dict1 = self.draw_msg1(temp_list)
        draw_dict2 = self.draw_msg2(temp_list)
        draw_dict3 = self.draw_msg3(temp_list)
        draw_dict4 = self.draw_msg4(temp_list)
        draw_dict5 = self.draw_msg5(temp_list)
        # 展示条形图
        self.draw(draw_dict1,draw_dict2,draw_dict3,draw_dict4,draw_dict5)


if __name__ == '__main__':
    wc_19 = World_COVID_19()
    while True:
        wc_19.run()
        print("程序沉睡中，半小时之后自动启动......")
        time.sleep(60*30)