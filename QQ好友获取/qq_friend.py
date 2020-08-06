# coding:utf-8
"""
主要注意的点是：session的cookie要时刻更新没有的cookie值，
并且要时刻更新session所需要的而且没有的cookie值。
update: 2020/7/29 17:13:42
author: 一只快死的猿
"""
import os
import re
import time
import json
import random
import warnings
import requests
from utils.misc import *
from utils.get_cookies import get_cookies


warnings.filterwarnings('ignore')


class QQZone():
    def __init__(self, **kwargs):
        self.info = 'QQZone'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.proxies = kwargs.get("proxies")

    def __initializePC(self):
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                        }
        self.xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
        self.qrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        self.qrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
        self.friend_url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi'
        self.group_url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/qqgroupfriend_extend.cgi'
        self.group_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/qqgroupfriend_groupinfo.cgi'

    def __decrypt_qrsig(self, qrsig):
        e = 0
        for c in qrsig:
            e += (e << 5) + ord(c)
        return 2147483647 & e

    def __get_g_tk(self, p_skey):
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
        return h & 2147483647

    def login(self, mode='pc', **kwargs):
        self.session.proxies.update(kwargs.get('proxies'))
        if mode == 'pc':
            self.__initializePC()
            # 获取pt_login_sig
            params = {
                        'proxy_url': 'https://qzs.qq.com/qzone/v6/portal/proxy.html',
                        'daid': '5',
                        'hide_title_bar': '1',
                        'low_login': '0',
                        'qlogin_auto_login': '1',
                        'no_verifyimg': '1',
                        'link_target': 'blank',
                        'appid': '549000912',
                        'style': '22',
                        'target': 'self',
                        's_url': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
                        'pt_qr_app': '手机QQ空间',
                        'pt_qr_link': 'https://z.qzone.com/download.html',
                        'self_regurl': 'https://qzs.qq.com/qzone/v6/reg/index.html',
                        'pt_qr_help_link': 'https://z.qzone.com/download.html',
                        'pt_no_auth': '0'
                    }
            res = self.session.get(self.xlogin_url, headers=self.headers, verify=False, params=params)
            pt_login_sig = get_cookies(res.cookies)['pt_login_sig']
            # 获得ptqrtoken
            params = {
                        'appid': '549000912',
                        'e': '2',
                        'l': 'M',
                        's': '3',
                        'd': '72',
                        'v': '4',
                        't': str(random.random()),
                        'daid': '5',
                        'pt_3rd_aid': '0'
                    }
            res = self.session.get(self.qrshow_url, headers=self.headers, verify=False, params=params)
            qrsig = get_cookies(res.cookies)['qrsig']
            ptqrtoken = self.__decrypt_qrsig(qrsig)
            # 保存二维码图片
            saveImage(res.content, os.path.join(self.cur_path, 'qrcode.jpg'))
            showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
            # 检测二维码状态
            while True:
                params = {
                            'u1': 'https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone',
                            'ptqrtoken': ptqrtoken,
                            'ptredirect': '0',
                            'h': '1',
                            't': '1',
                            'g': '1',
                            'from_ui': '1',
                            'ptlang': '2052',
                            'action': '0-0-' + str(int(time.time())),
                            'js_ver': '19112817',
                            'js_type': '1',
                            'login_sig': pt_login_sig,
                            'pt_uistyle': '40',
                            'aid': '549000912',
                            'daid': '5',
                            'has_onekey': '1'
                        }
                res = self.session.get(self.qrlogin_url, headers=self.headers, verify=False, params=params)
                if '登录成功' in res.text:
                    break
                elif '二维码已经失效' in res.text:
                    raise RuntimeError('Fail to login, qrcode has expired...')
                time.sleep(2)
            # 登录成功
            qq_number = re.findall(r'&uin=(.+?)&service', res.text)[0]
            url_refresh = res.text[res.text.find('http'): res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
            self.session.get(url_refresh, headers=self.headers, verify=False)
            removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
            print('[INFO]: Account -> %s, login successfully...' % qq_number)
            uin = get_cookies(self.session.cookies)["uin"][1:]
            p_skey = get_cookies(self.session.cookies)["p_skey"]
            g_tk = self.__get_g_tk(p_skey)
            return uin, g_tk
        else:
            raise ValueError('Unsupport argument in QQZone.login : mode %s, expect <mobile> or <pc>...' % mode)

    def get_friends_info(self, uin, g_tk):
        params = {
            "uin": uin,
            "do": "1",
            "rd": str(random.random()),
            "fupdate": "1",
            "clean": "1",
            "g_tk": g_tk,
        }
        res = self.session.get(self.friend_url, headers=self.headers, verify=False, params=params)
        result = re.findall(r"_Callback\((.*)\);", res.text, re.S)
        result = json.loads(result[0])
        friend_info = {}
        for item in result["data"]["items_list"]:
            friend_info[item["uin"]] = item["name"]
        return friend_info

    def get_gid(self, uin, g_tk):
        params = {
            "uin": uin,
            "do": "1",
            "rd": str(random.random()),
            "fupdate": "1",
            "clean": "1",
            "g_tk": g_tk,
        }
        res = self.session.get(self.group_url, headers=self.headers, verify=False, params=params)
        result = re.findall(r"_Callback\((.*)\);", res.text, re.S)
        result = json.loads(result[0])
        gid_info = {}
        for item in result["data"]["group"]:
            gid_info[item["groupcode"]] = item["groupname"]
        return gid_info

    def get_group_friend(self, uin, g_tk, gid):
        params = {
            "uin": uin,
            "gid": gid,
            "fupdate": "1",
            "type": "1",
            "g_tk": g_tk
        }
        res = self.session.get(self.group_friend, headers=self.headers, verify=False, params=params)
        result = re.findall(r"_Callback\((.*)\);", res.text, re.S)
        result = json.loads(result[0])
        gid_info = {}
        for item in result["data"]["friends"]:
            gid_info[item["fuin"]] = item["name"]
        return gid_info

    def run(self):
        # 获取必要参数
        uin, g_tk = self.login(proxies=self.proxies)
        # 获取朋友
        friend_info = self.get_friends_info(uin, g_tk)
        # 获取群
        gid_info = self.get_gid(uin, g_tk)
        # 获取不是好友的群友
        group_friend_info = {}
        for gid, gname in gid_info.items():
            group_friend_info[gname] = self.get_group_friend(uin, g_tk, gid)
        print("QQ好友：", friend_info)
        print("QQ群组：", gid_info)
        print("QQ群友：", group_friend_info)


if __name__ == '__main__':
    ip_pool = [
        {"2f81s4rp": "http://58.218.200.248:5383"},
        {"vH7w9oj1": "http://58.218.200.248:3231"},
        {"ZP4w0hLf": "http://58.218.200.229:3830"},
        {"MoBdIk5z": "http://58.218.200.237:10503"},
        {"qA8rM7i0": "http://58.218.200.237:4868"},
        {"9rhaRjFD": "http://58.218.200.248:4815"},
        {"BCORHl7Q": "http://58.218.200.247:6881"},
        {"vD4l6H1B": "http://58.218.200.214:9810"},
        {"q6LzXlPk": "http://58.218.200.229:2803"},
        {"lJ2C471O": "http://58.218.200.214:3853"},
    ]
    proxy_ip = random.choice(ip_pool)
    qz = QQZone(proxies=proxy_ip)
    qz.run()