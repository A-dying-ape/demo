# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import os
import sys
import time
import json
import random
import config
import requests
sys.path.append("../common")
sys.path.append("../../common")
from extend import Extend
from base_script import BaseScript
from inform_model import Inform


class AdapterBusiness(Extend, BaseScript, Inform):
    """
    对hook业务进行适配，分发到对应的业务链上进行hook
    """
    Adapter = dict()

    def __init__(self, filename, device, url, full_path=""):
        Extend.__init__(self)
        BaseScript.__init__(self, filename, device, url, full_path)
        Inform.__init__(self, config.inform_url)
        for i in dir(self):
            self.Adapter[i] = getattr(self, i)

    def hooker_video_url(self):
        """
        hook视频播放地址
        """
        self.frida_object.exports.hooker_video_url(
            self.device,
            self.get_response
        )

    def hooker_video_goods(self):
        """
        hook视频挂链
        """
        self.frida_object.exports.hooker_video_goods(
            self.device,
            self.get_response
        )

    def hooker_topic_activity(self, tab=1):
        """
        hook视频活动
        """
        self.frida_object.exports.hooker_topic_activity(
            self.device,
            tab,
            self.get_response
        )

    def hooker_topic_topic(self):
        """
        hook视频话题
        """
        self.frida_object.exports.hooker_topic_topic(
            self.device,
            self.get_response
        )

    def hooker_getcookie(self):
        """
        hook微信cookie
        """
        self.frida_object.exports.hooker_getcookie(
            "cookie",
            "v2_060000231003b20faec8c5e08a18c4dcc60cec31b077b2e0eab771d78025b3800ae7b330f30e@finder"
        )

    def hooker_product_third(self):
        """
        hook带货中心商品详情
        """
        self.frida_object.exports.hooker_product_third(
            self.device,
            "wx2cea70df4257bba8",
            self.vx_cookie,
            self.get_response
        )

    def hooker_product_takecenter(self):
        """
        hook带货中心商品列表
        """
        self.frida_object.exports.hooker_product_takecenter(
            self.device,
            "wx2cea70df4257bba8",
            self.vx_cookie,
            self.get_response
        )

    def hooker_product_store(self):
        """
        hook微信小商店信息
        """
        self.frida_object.exports.hooker_product_store(
            self.device,
            "wx34345ae5855f892d",
            self.get_response
        )

    def hooker_product_info(self):
        """
        hook微信小商店商品详情
        """
        self.frida_object.exports.hooker_product_info(
            self.device,
            "wx34345ae5855f892d",
            self.get_response
        )

    def hooker_product_list(self):
        """
        hook微信小商店商品列表
        """
        self.frida_object.exports.hooker_product_list(
            self.device,
            "wx34345ae5855f892d",
            self.get_response
        )

    def hooker_live_tab(self):
        """
        hook直播分类
        """
        self.frida_object.exports.hooker_live_tab(self.device)

    def hooker_live_square(self):
        """
        hook直播广场
        """
        for i in self.get_response.get("data").get("cates"):
            if i.get("cateid") > 10:
                continue
            self.check_frida()
            self.frida_object.exports.hooker_live_square(
                self.device,
                {
                    "VHZ": i.get("cateid"),
                    "VIa": i.get("catename"),
                    "VIb": False,
                    "VIc": False,
                    "VId": False,
                    "VIe": False,
                    "VIf": [],
                    "VIg": 0,
                    "data": "",
                    "includeUnKnownField": False,
                    "object_id": 0
                }
            )
            self.wait()

    def hooker_live_goods(self):
        """
        hook直播带货
        """
        self.frida_object.exports.hooker_live_goods(
            self.device,
            self.username,
            self.get_response
        )

    def hooker_live_contribution(self):
        """
        hook直播间热度贡献榜
        """
        self.frida_object.exports.hooker_live_contribution(
            self.device,
            self.username,
            self.get_response
        )

    def hooker_live_barrage(self):
        """
        hook直播间弹幕
        """
        self.frida_object.exports.hooker_live_barrage(
            self.device,
            self.username,
            self.get_response
        )

    def hooker_live_info(self):
        """
        hook直播间信息
        """
        self.frida_object.exports.hooker_live_info(
            self.device,
            self.username,
            self.get_response
        )

    def hooker_detail_goods(self):
        """
        hook主页商品
        """
        self.frida_object.exports.hooker_detail_goods(
            self.device,
            self.get_response
        )

    def hooker_detail_video(self):
        """
        hook主页视频
        """
        self.frida_object.exports.hooker_detail_video(
            self.device,
            self.get_response
        )

    def hooker_video_comment(self):
        """
        hook视频评论
        """
        self.frida_object.exports.hooker_video_comment(
            self.device,
            False,
            self.get_response
        )

    def adapter_business(self):
        """
        hook业务分发
        """
        self.check_frida()
        self.get_params()
        if self.device == "comment":
            self.Adapter["hooker_video_comment"]()
            self.wait()
        elif self.device == "detail":
            self.Adapter["hooker_detail_video"]()
            self.wait()
            self.check_frida()
            self.Adapter["hooker_detail_goods"]()
            self.wait()
        elif self.device == "hourlist":
            if not (self.vx_cookie and os.path.exists(self.cookie_file)):
                self.get_cookie()
                self.wait_cookie()
            content = self.make_hourlist_response(self.get_response)
            self.post_response = content
            self.Handle[self.device](config.post_url.get(self.device).format(self.uuid, self.addr))
        elif self.device == "livebarrage":
            self.Adapter["hooker_live_barrage"]()
            self.wait()
        elif self.device == "liveinfo":
            self.Adapter["hooker_live_info"]()
            self.wait()
        elif self.device == "livecontribution":
            self.Adapter["hooker_live_contribution"]()
            self.wait()
        elif self.device == "livegoods":
            self.Adapter["hooker_live_goods"]()
            self.wait()
        elif self.device == "livesquare":
            self.Adapter["hooker_live_tab"]()
            self.wait()
            self.Adapter["hooker_live_square"]()
        elif self.device == "product":
            if self.get_response.get("data").get("method") == "GetShopCenter":
                self.Adapter["hooker_product_store"]()
            elif self.get_response.get("data").get("method") == "BatchGetProductByBizUin":
                self.Adapter["hooker_product_list"]()
            elif self.get_response.get("data").get("method") == "GetProduct":
                self.Adapter["hooker_product_info"]()
            elif self.get_response.get("data").get("method") == "EcGetItemList":
                if self.vx_cookie:
                    self.Adapter["hooker_product_takecenter"]()
                else:
                    self.get_cookie()
                    self.wait_cookie()
                    self.check_frida()
                    self.Adapter["hooker_product_takecenter"]()
            elif self.get_response.get("data").get("method") == "EcGetItemDetail":
                if self.vx_cookie:
                    self.Adapter["hooker_product_third"]()
                else:
                    self.get_cookie()
                    self.wait_cookie()
                    self.check_frida()
                    self.Adapter["hooker_product_third"]()
            else:
                self.logger.error("product business undefined method %s ." % self.get_response.get("data").get("method"))
            self.wait()
        elif self.device == "topic":
            if int(self.get_response["data"].get("type")) == 1:
                self.Adapter["hooker_topic_topic"]()
            elif int(self.get_response["data"].get("type")) == 2:
                self.Adapter["hooker_topic_activity"](1)
                self.wait()
                self.check_frida()
                self.Adapter["hooker_topic_activity"](2)
            else:
                self.logger.error("topic business undefined type %s ." % self.get_response["data"].get("type"))
            self.wait()
        elif self.device == "videogoods":
            self.Adapter["hooker_video_goods"]()
            self.wait()
        elif self.device == "videourl":
            self.Adapter["hooker_video_url"]()
            self.wait()
        else:
            self.logger.error("can't find this device: %s" % self.device)
        time.sleep(
            random.randint(
                self.sleep_time.get(self.device).get("begin"),
                self.sleep_time.get(self.device).get("end")
            )
        )


class HandleBusiness(AdapterBusiness):
    """
    对send回来的数进行适配，分发到对应的业务链上处理
    """
    Handle = dict()

    def __init__(self, filename, device, url, full_path=""):
        AdapterBusiness.__init__(self, filename, device, url, full_path)
        for i in dir(self):
            self.Handle[i] = getattr(self, i)

    def cookie(self, post_url):
        """
        微信cookie
        :param post_url : 数据回调地址
        """
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.get_cookie(self.post_response.get("result").get("VWA"))

    def comment(self, post_url):
        """
        视频评论
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def detail(self, post_url):
        """
        主页信息
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def hourlist(self, post_url):
        """
        小时榜
        :param post_url : 数据回调地址
        """
        for c in self.post_response:
            c["username"] = self.get_response["data"].get("username")
            c["curtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
            status = requests.post(post_url, json.dumps(c, ensure_ascii=False).encode("utf-8").decode("latin1"))
            self.logger.info(str(c.get("device")) + str(status))

    def livebarrage(self, post_url):
        """
        直播间弹幕
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def liveinfo(self, post_url):
        """
        直播间信息
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        if self.device == self.post_response.get("device"):
            self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def livecontribution(self, post_url):
        """
        直播间热度贡献榜
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def livegoods(self, post_url):
        """
        直播间带货
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def livesquare(self, post_url):
        """
        直播广场
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        if int(self.post_response.get("type")) == 2:
            if int(self.post_response.get("hasnext")) == 0:
                self.flag = True
            else:
                self.wait_count = 0
        else:
            self.flag = True
            self.wait_count = 0
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def product(self, post_url):
        """
        微信小商店和带货中心
        :param post_url : 数据回调地址
        """
        if self.post_response.get("method") == "EcGetItemList" or self.post_response.get("method") == "EcGetItemDetail":
            if self.post_response.get("flag") in ["-330", "-333", "-334"] and os.path.exists(self.cookie_file):
                os.remove(self.cookie_file)
                self.vx_cookie = None
                self.logger.info("the cookie has expired. obtain it again.")
                self.flag = True
            else:
                status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
                self.flag = True
                self.logger.info(str(self.post_response.get("device")) + str(status))
        else:
            if self.post_response.get("method") == "BatchGetProductByBizUin" and self.post_response.get("next_key") == "" and int(
                    self.post_response.get("page_num")) > 0:
                self.flag = True
            elif self.post_response.get("method") == "cookie":
                self.get_cookie(self.post_response.get("result").get("VWA"))
                self.flag = True
            else:
                status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
                if self.post_response.get("method") == "GetProduct" or self.post_response.get("method") == "GetShopCenter":
                    self.flag = True
                self.logger.info(str(self.post_response.get("device")) + str(status))
        self.wait_count = 0
        self.remove_monitor = False

    def topic(self, post_url):
        """
        话题和活动
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        if int(self.post_response.get("continueFlag")) == 0:
            self.flag = True
        else:
            self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def videogoods(self, post_url):
        """
        视频挂链
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def videourl(self, post_url):
        """
        视频播放地址
        :param post_url : 数据回调地址
        """
        status = requests.post(post_url, json.dumps(self.post_response).encode("utf-8").decode("latin1"))
        self.flag = True
        self.wait_count = 0
        self.remove_monitor = False
        self.logger.info(str(self.post_response.get("device")) + str(status))

    def handle_business(self):
        """
        send数据适配主逻辑
        """
        try:
            post_url = config.post_url.get(self.post_response.get("device")).format(self.uuid, self.addr)
        except Exception as e:
            self.logger.info("currently, it is an internal service")
            post_url = None
        self.Handle[self.post_response.get("device")](post_url)