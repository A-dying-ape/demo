import requests
import json
import re
from setting import HEADERS, ACCOUNT, PASSWORD
from util.hash import md5hash
from util.dealjson import deal_json_invaild


class Login():
    def __init__(self, session):
        self.session = session
        self.formhash_url = "https://www.epwk.com/login.html"
        self.login_url = "https://www.epwk.com/index.php"

    def hash_pwd(self, pwd):
        byte_pwd = pwd.encode()
        return md5hash(byte_pwd)

    def get_formhash(self):
        response = self.session.get(self.formhash_url, headers=HEADERS)
        res = re.findall("<input type=\"hidden\" name=\"formhash\" id=\"formhash\" value=\"(.*?)\">", response.text)
        return res

    def login(self):
        params = {"do": "login"}
        data = {
            "formhash": self.get_formhash(),
            "txt_account": ACCOUNT,
            "pwd_password": self.hash_pwd(PASSWORD),
            "login_type": "3",
            "ckb_cookie": "0",
            "hdn_refer": "https://task.epwk.com/wuxian/",
            "txt_code":"",
            "pre": "login",
            "inajax": "1",
        }
        response = self.session.post(self.login_url, headers=HEADERS, params=params, data=data)
        self.check_login(response.content.decode("unicode_escape"))

    def check_login(self, status_msg):
        jstr = deal_json_invaild(status_msg)
        jstr = json.loads(jstr)
        if jstr.get("status") != 1:
            print("登陆失败！错误提示:%s" %jstr.get("msg"))
        else:
            print("登陆成功！当前用户%s" %jstr.get("data").get("username"))

    def run(self):
        self.login()