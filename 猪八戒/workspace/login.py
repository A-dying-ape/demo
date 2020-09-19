import time
import random
import json
from util.img_handl import showImage, removeImage, saveImage


class Login():
    def __init__(self, session, headers, IP_POOL):
        self.session = session
        self.headers = headers
        self.IP_POOL = IP_POOL
        self.token_url = "https://account.zbj.com/login/QrcodeFromWx"
        self.code_url = "https://login.zbj.com/applogin/QrcodeFromApp"
        self.login_url = "https://account.zbj.com/login/QrWxConnect"
        self.sign_url = "https://tongxin.zbj.com/api/txtim/getUserSign"
        self.a2_url = "https://webim.tim.qq.com/v4/openim/login"
        self.im_url = "https://profile.zbj.com/api/imKeyService/getImKey"
        self.gpoll_url = "https://webim.tim.qq.com/v4/openim/getlongpollingid"
        self.poll_url = "https://webim.tim.qq.com/v4/openim/longpolling"

    def get_token(self):
        params = {
            "ttt": str(time.time() * 1000),
            "flag": "1",
            "src": "1"
        }
        self.session.proxies.update(random.choice(self.IP_POOL))
        response = self.session.get(self.token_url, headers=self.headers, params=params)
        token_dict = json.loads(response.text)
        return token_dict.get("token")

    def get_code(self, token):
        params = {
            "token": str(token)
        }
        response = self.session.get(self.code_url, headers=self.headers, params=params)
        saveImage(response.content, "./code.jpg")
        showImage("./code.jpg")

    def login(self, token):
        params = {
            "ttt": str(int(time.time() * 1000)),
            "token": str(token),
            "flag": "1",
            "src": "1"
        }
        while True:
            time.sleep(1)
            response = self.session.get(self.login_url, headers=self.headers, params=params)
            flag_dict = json.loads(response.text)
            if flag_dict.get("code") != 0:
                break
        removeImage("./code.jpg")

    def check_ok(self):
        if self.session.cookies.get("nickname"):
            print("登陆成功！当前账号为:" + self.session.cookies.get("nickname"))
        else:
            print("登陆失败！未知错误！")

    def run(self):
        token = self.get_token()
        self.get_code(token)
        self.login(token)
        self.check_ok()