# coding:utf-8
"""
主要注意的点是：session的cookie要时刻更新没有的cookie值，
并且要时刻更新session所需要的而且没有的cookie值。
update: 2020/8/22 17:01:42
author: 一只快死的猿
"""
import os
import re
import time
import random
from setting import HEADERS
from utils.misc import saveImage, showImage, removeImage
from utils.get_cookies import get_cookies


headers = HEADERS


class QQZone():
    def __init__(self, **kwargs):
        self.cur_path = os.getcwd()
        self.proxies = kwargs.get("proxies")
        self.session = kwargs.get("session")

    def __initializePC(self):
        self.xlogin_url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin'
        self.qrshow_url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        self.qrlogin_url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'

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
            res = self.session.get(self.xlogin_url, headers=headers, verify=False, params=params)
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
            res = self.session.get(self.qrshow_url, headers=headers, verify=False, params=params)
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
                res = self.session.get(self.qrlogin_url, headers=headers, verify=False, params=params)
                if '登录成功' in res.text:
                    break
                elif '二维码已经失效' in res.text:
                    raise RuntimeError('Fail to login, qrcode has expired...')
                time.sleep(1)
            # 登录成功
            qq_number = re.findall(r'&uin=(.+?)&service', res.text)[0]
            url_refresh = res.text[res.text.find('http'): res.text.find('pt_3rd_aid=0')] + 'pt_3rd_aid=0'
            self.session.get(url_refresh, headers=headers, verify=False)
            removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
            print('[OK]: Account -> %s, login successfully...' % qq_number)
            p_skey = get_cookies(self.session.cookies)["p_skey"]
            g_tk = self.__get_g_tk(p_skey)
            return g_tk
        else:
            raise ValueError('Unsupport argument in QQZone.login : mode %s, expect <mobile> or <pc>...' % mode)

    def run(self):
        g_tk = self.login(proxies=self.proxies)
        return g_tk



