import requests
import re
import execjs
import json
import win32api
import win32con
import time
import threading
import queue
import random
import create_ua


q = queue.Queue()
COOKIES_FILE_PATH = 'taobao_cookies.txt'


class TB_Login():
    """
    淘宝登录类，获取cookie
    """
    def __init__(self, account, password, chrome_version, updata_log, proxy):
        self.account = account
        self.password = password
        self.chrome_version = chrome_version
        self.proxy = proxy
        self.ua = "137#cuE9hE9oUjRmcoeAbEHcU+g6IQk/KU5VgMXaUTqlIidDEj4t1G4DtO8KTmMpRbkKB5P3mNUwZaz2OqijFRun3S4RN/M4hnUJT/uGzABCZBbAVSkUo5UI4Lec8TeODyzE3cmlwhp5voirs3ayaR3PK+a67/X82nREE3k7UzE8q4nRDZw2vI5NAJXA2U5AX99KPg+S3TTyi4WfbPMScLXE1nGWumU6oMQDvXqqb1gdvfRpbPd+HUf6VfEHYUwGjs8Gfuk41zsgiXnDNhnTFkuaJZqtAx3cAa1GBLcHYQwbqIRhdUeyhBfkqZhFQ663UPnCrBwj7AHK5J6zfLsX+XGTJXgEpcYpIwWGTqWupmgjTy3YlsWf49LLSP7zBGqx0CsmiRWnUMdK+r5D/NODLhLwWwjq8osSLqgEW6RHqfWk0ejwqkQ2pXSWKn8qHcy0xJD12HbJ7s52NMRUbLPaghVbnA7J8sNGjhmmV9VO3AmE0l5RoHPBooJwncOqn0ZzOGzZw5XGpneInVXI2eaODt41SFPEB8t6y1EgjSpWhYUuuqoYFob6R3vQYTUx1lg8pTgpRefoMDe9pEfB1o3T7BqV5SOx1lgypppE24hFLS7ppRUc1Aey+tIvYSUxKh7F5XWcQeVo+ZDVpRUm1ATyuXiVYSUF2jMSrEZj3jmqVXTn/0Jc1Iei+cqpYSJS1qQiVppcQenJ+ZXVpkUm1AEy+piGUo4VLm99iIS27I0FSbciY4MMNUNCzXJOB56AThBhy5R4ZZttLJPaPFidvHqsLQuDh1zwqX+5O1PHrfm7v+FnwxRZJ1KSaG3DkwiF8azFGhcP6wzbqZXdQQr16gPC3ho/hk/JTo3RTIlxYrIVYWenedsczmoaAw0DeXadavrNBlRzZuxueZkDCUf0OrPLl/K9TFoLDnT/CT+UlvGByeujyYozj6wzgeOeil2/NdU5+cVNt6lDzQ3veNQH4ci3erT6R9DdlnG52WBeSwb59fJjlZRjAU4i79D6kfCV1X4urweCKnw3RaPvpueeoLJuGJXNliQ3eXoeAp5JIZ7K1a7Ojn+6eflLNiSd1/nfmnING7WhG32V37c4OOqUIr1l0wyePUhuNDaOgBqZXWwfpqwtwjwVxQYyj8SN451ZGisFm+lLrdPZk2S/8jmindLbbEOh2uF1MfGOBE5+8KuxXGL8Rl/MERBSIoSg7Mrl7OtdWG4cJwr25OI2fMcCBBHIE1ks19HGesgF7nfTDSja+xmjQWXxAB56QXc1AK5oRYugKbXW/a90Tbgq2noLNRRoNK1FUv4Zr+U3zoBzGKpZms4lnrAnRUNX6lFEVOw0FQzaDJjTd2zHhQ4+ceygzmMakLcHYq5NBeE4EEeOMG1VciRatjGBUeBYXdnfH3JxdDHnKfp4t2/GLV0oEha/o5BPi7K4jju7xtod71W5HLMl2+ErLuqAxaYl/KG+uSK1Ks0QeZrXV1WXkG1XEAtgI9b4Et/H0pTdJSpmo0kvh3pvknxs9AGk9qAqYd1AJA8OHfVk5VEAj/4S8Sclo94HB/w11J5Bm0XTtB=="
        self.session = requests.session()
        self.login_html = "https://login.taobao.com/member/login.jhtml"
        self.user_check_url = "https://login.taobao.com/newlogin/account/check.do?appName=taobao&fromSite=0"
        self.tb_login_url = "https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0"
        self.vst_url = 'https://login.taobao.com/member/vst.htm?st={}'
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'
        self.password2 = self._encrypt_password()
        self.lc_data = self._create_data()
        self.updata_log = updata_log

    def _encrypt_password(self):
        """
        对淘宝密码进行加密
        :return: 加密后的结果
        """
        with open("./password2.js", mode="r", encoding='UTF-8') as f:
            content = f.read()
        pwd2js = execjs.compile(content)
        return pwd2js.call("begin", self.password)

    @staticmethod
    def _get_screen():
        """
        捕获屏幕大小
        :return:
        """
        x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        return str(x) + "x" + str(y)

    def _create_data(self):
        """
        创建检验滑块和登录所需要的参数
        :return:
        """
        headers = {
            "user-agent": self.chrome_version
        }
        response = self.session.get(self.login_html, headers=headers, proxies=self.proxy)
        return {
            "loginId": self.account,
            "keepLogin": "false",
            "ua": self.ua,
            "umidGetStatusVal": "255",
            "screenPixel": self._get_screen(),
            "navlanguage": "zh-CN",
            "navUserAgent": self.chrome_version,
            "navPlatform": "Win32",
            "appName": "taobao",
            "appEntrance": "taobao_pc",
            "_csrf_token": re.findall(r"\"_csrf_token\":\"(.*?)\"", response.text)[0],
            "umidToken": re.findall(r"\"umidToken\":\"(.*?)\"", response.text)[0],
            "hsiz": re.findall(r"\"hsiz\":\"(.*?)\"", response.text)[0],
            "bizParams": "",
            "style": "default",
            "appkey": "00000000",
            "from": "tbTop",
            "isMobile": "false",
            "lang": "zh_CN",
            "fromSite": "0",
            "returnUrl": "https://ai.taobao.com/?pid=mm_130402922_1111150093_109790500145&union_lens=lensId%3APUB%401585398442%400b0b0e45_0e0f_171211c6ac6_04ba%4001"
        }

    def user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = self.lc_data
        try:
            response = self.session.post(self.user_check_url, data=data, proxies=self.proxy)
            response.raise_for_status()
        except Exception as e:
            raise e
        check_resp_data = response.json()['content']['data']
        needcode = False
        # 判断是否需要滑块验证，一般短时间密码错误多次可能出现
        if 'isCheckCodeShowed' in check_resp_data:
            needcode = True
        return needcode

    def verify_login(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        headers = {
            'Origin': 'https://login.taobao.com',
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': self.chrome_version,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9HjW9WC&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
        }
        data = self.lc_data
        data["password2"] = self.password2
        try:
            response = self.session.post(self.tb_login_url, headers=headers, data=data, proxies=self.proxy)
            response.raise_for_status()
        except Exception as e:
            raise e
        # 提取申请st码url
        apply_st_url = response.json()['content']['data']['asyncUrls'][0]
        # 存在则返回
        if apply_st_url:
            return apply_st_url
        else:
            print('用户名密码验证失败！response：{}'.format(response.text))

    def _save_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        with open(COOKIES_FILE_PATH, 'a', encoding='utf-8') as file:
            file.write(str(cookies_dict) + "\n")

    def get_st_code(self):
        """
        请求st码申请地址，获取st码
        :return: st码
        """
        apply_st_url = self.verify_login()
        try:
            response = self.session.get(apply_st_url, proxies=self.proxy)
            response.raise_for_status()
        except Exception as e:
            raise e
        st_match = re.search(r'"data":{"st":"(.*?)"}', response.text)
        if st_match:
            return st_match.group(1)
        else:
            print('获取st码失败！response：{}'.format(response.text))

    def login_tb(self):
        """
        登录住逻辑
        :return:
        """
        try:
            self.user_check()
        except:
            self.updata_log.emit(">>被防爬了，请设置代理！")
            return
        st = self.get_st_code()
        headers = {
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive',
            'User-Agent': self.chrome_version
        }
        try:
            response = self.session.get(self.vst_url.format(st), headers=headers, proxies=self.proxy)
            response.raise_for_status()
        except:
            print("获取淘宝首页的URL失败")
        # 登录成功，提取跳转淘宝用户主页url
        my_taobao_match = re.search(r'top.location.href = "(.*?)"', response.text)
        if my_taobao_match:
            self.my_taobao_url = my_taobao_match.group(1)
            self._save_cookies()
            return True
        else:
            print("登录失败")

    def check_login(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': self.chrome_version
        }
        try:
            response = self.session.get(self.my_taobao_url, headers=headers, proxies=self.proxy)
            response.raise_for_status()
        except :
            print("获取淘宝昵称失败")
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            self.updata_log.emit('>>登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            print('获取淘宝昵称失败！response：{}'.format(response.text))

    def run(self):
        if self.login_tb():
            self.check_login()


def create_proxy():
    """
    构建代理
    :return: 代理
    """
    with open("ip_pool", "r", encoding="utf-8") as f:
        content = f.read()
    return {"http": random.choice(eval(content))}


def main(q, updata_log, proxy_flag):
    count = 0
    while True:
        if q.empty():
            time.sleep(0.5)
            if count >= 5:
                break
            count += 1
        else:
            q_temp = q.get()
            account = q_temp["account"]
            password = q_temp["password"]
            chrome_version = create_ua.user_agent()
            proxy = None
            if proxy_flag:
                proxy = create_proxy()
            tb = TB_Login(account, password, chrome_version, updata_log, proxy)
            tb.run()


def run_cookie(account_list, updata_log, login_count, proxy_flag):
    t_list = []
    try:
        for a in account_list:
            temp_dict = {}
            account = a.split("||")[0]
            password = a.split("||")[1]
            temp_dict["account"] = account
            temp_dict["password"] = password
            q.put(temp_dict)
    except:
        updata_log.emit(">>账号密码文件格式错误")
        return
    else:
        login_count.emit(str(q.qsize()))
        if q.qsize() <= 6:
            for i in range(q.qsize()):
                t_list.append(threading.Thread(target=main, args=(q, updata_log, proxy_flag)))
            for t in t_list:
                t.start()
        else:
            for i in range(6):
                t_list.append(threading.Thread(target=main, args=(q, updata_log, proxy_flag)))
            for t in t_list:
                t.start()
