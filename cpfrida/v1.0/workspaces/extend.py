# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import os
import re
import time
import json
import urllib
import requests
from params import FixedParams

requests.packages.urllib3.disable_warnings()


class Extend(FixedParams):
    """
    整个流程多余的一些扩展功能
    """

    def __init__(self):
        FixedParams.__init__(self)

    def wait_cookie(self):
        """
        等待cookie的延时
        """
        while self.vx_cookie is None:
            time.sleep(0.1)

    def adapter_cookie(self):
        """
        适配cookie符合不同业务
        """
        if self.device == "product":
            self.vx_cookie = urllib.parse.unquote(re.search(r"_finder_auth=(.*?);", self.vx_cookie).group(1))

    def get_cookie(self, url=None):
        """
        获取cookie
        :param url : cookie获取地址
        """
        if os.path.exists(self.cookie_file):
            with open(self.cookie_file, "r") as f:
                cookie = f.read()
                self.vx_cookie = cookie
                self.adapter_cookie()
        else:
            if url is None:
                self.Adapter["hooker_getcookie"]()
                getattr(self, "wait")()
            else:
                headers = dict()
                headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
                headers["Accept-Encoding"] = "gzip, deflate, br"
                headers["Accept-Language"] = "zh-CN,zh;q=0.9"
                headers["Cache-Control"] = "max-age=0"
                headers["Connection"] = "keep-alive"
                headers["Host"] = "channels.weixin.qq.com"
                headers["If-None-Match"] = 'W/"734-LvtVz8A4IfS+SR9AEQNZNNI4NYw"'
                headers["sec-ch-ua"] = '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'
                headers["sec-ch-ua-mobile"] = "?0"
                headers["sec-ch-ua-platform"] = '"Windows"'
                headers["Sec-Fetch-Dest"] = "document"
                headers["Sec-Fetch-Mode"] = "navigate"
                headers["Sec-Fetch-Site"] = "same-origin"
                headers["Sec-Fetch-User"] = "?1"
                headers["Upgrade-Insecure-Requests"] = "1"
                headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
                resp = requests.get(url, headers=headers, verify=False)
                cookie = resp.headers.get("Set-Cookie")
                with open(self.cookie_file, "w", encoding="utf-8") as f:
                    f.write(str(cookie))
                    self.vx_cookie = cookie
                    self.adapter_cookie()
                    self.logger.info("save cookies locally.")

    def get_listhour_web(self, username, group_id, loop=None):
        """
        获取小时榜
        :param username : 主播username
        :param group_id : 赛区id
        :param loop : 某一场次
        :return : 小时榜json， 场次
        """
        url = "https://channels.weixin.qq.com/mobile-support/api/heat-race/board-list"
        headers = dict()
        headers["Host"] = "channels.weixin.qq.com"
        headers["Connection"] = "keep-alive"
        headers["Content-Length"] = "281"
        headers["Accept"] = "application/json, text/plain, */*"
        headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; Android 10; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3189 MMWEBSDK/20220204 Mobile Safari/537.36 MMWEBID/2924 MicroMessenger/8.0.20.2100(0x28001439) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
        headers["Content-Type"] = "application/json"
        headers["Origin"] = "https://channels.weixin.qq.com"
        headers["X-Requested-With"] = "com.tencent.mm"
        headers["Sec-Fetch-Site"] = "same-origin"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Dest"] = "empty"
        headers[
            "Referer"] = "https://channels.weixin.qq.com/mobile-support/pages/race/hour?finder_activity_id=FinderLiveActivityHourBoardLong3_opweyuy2l_1643084450&BannerId=finderactivity_1_13783311145357543482&finderusername=%s" % username
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Accept-Language"] = "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        headers["Cookie"] = self.vx_cookie
        if int(loop) < 1080:
            loop = int(
                (int(time.time()) - int(time.mktime(time.strptime("2022-01-23 15:00:00", "%Y-%m-%d %H:%M:%S")))) / 3600)
        data = dict()
        data["activity_id"] = "FinderLiveActivityHourBoardLong3_opweyuy2l_1643084450"
        data["group_id"] = int(group_id)
        data["stage_id"] = "LiveActivityStageLoop_" + str(loop)
        data["anchor_finder_username"] = username
        data["base_req"] = dict()
        data["base_req"]["app_name"] = "NativeHourlyRank"
        response = json.loads(requests.post(url, headers=headers, json=data, verify=False).text)
        return response.get("data").get("board_items"), response.get("data").get("self_item"), loop

    def make_hourlist_response(self, response):
        """
        封装小时榜回调数据
        :param response : 队列请求数据
        :return result : 迭代器
        """
        try:
            for k, v in self.area_tab.items():
                board_items, self_item, loop = self.get_listhour_web(response["data"].get("username"), v,
                                                                     response["data"].get("loop"))
                time.sleep(self.sleep_time.get("hourlist").get("each"))
                result = dict()
                result["result"] = dict()
                result["result"]["group_name"] = k
                result["result"]["board_items"] = board_items
                result["result"]["self_item"] = self_item
                result["loop"] = loop
                result["device"] = "hourlist"
                yield result
        except Exception as e:
            os.remove(self.cookie_file)
            self.vx_cookie = None
            self.logger.info("the cookie has expired. obtain it again.")
            self.adapter_business()

    def handle_inform_text(self, **kwargs):
        """
        处理通知
        :param kwargs : 修改目标
        :return 格式化后的消息
        """
        self.inform_text["content"]["post"]["zh_cn"]["content"][0][1]["text"] = kwargs["device"]
        self.inform_text["content"]["post"]["zh_cn"]["content"][3][1]["text"] = kwargs["err_msg"]
        return self.inform_text
