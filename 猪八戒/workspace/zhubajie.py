import requests
import random
import time
import json
from ip_pool import IP_POOL
from util.img_handl import showImage, removeImage, saveImage



session = requests.session()


class Zhubajie_Spider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
            "Referer": "https://account.zbj.com/login?fromurl=http://i.zbj.com/"
        }
        self.token_url = "https://account.zbj.com/login/QrcodeFromWx"
        self.code_url = "https://login.zbj.com/applogin/QrcodeFromApp"
        self.login_url = "https://account.zbj.com/login/QrWxConnect"
        self.sign_url = "https://tongxin.zbj.com/api/txtim/getUserSign"
        self.a2_url = "https://webim.tim.qq.com/v4/openim/login"
        self.im_url = "https://profile.zbj.com/api/imKeyService/getImKey"
        self.gpoll_url= "https://webim.tim.qq.com/v4/openim/getlongpollingid"
        self.poll_url = "https://webim.tim.qq.com/v4/openim/longpolling"
        self.sendmsg = "https://webim.tim.qq.com/v4/openim/sendmsg"

    def get_token(self):
        params = {
            "ttt": str(time.time() * 1000),
            "flag": "1",
            "src": "1"
        }
        session.proxies.update(random.choice(IP_POOL))
        response = session.get(self.token_url, headers=self.headers, params=params)
        token_dict = json.loads(response.text)
        return token_dict.get("token")

    def get_user_sign(self):
        response = session.get(self.sign_url, headers=self.headers)
        usersig = json.loads(response.text).get("data").get("sig")
        identifier = json.loads(response.text).get("data").get("openId")
        openId = json.loads(response.text).get("data").get("openId")
        return usersig, identifier, openId

    def get_a2(self, usersig, identifier):
        params = {
            "websdkappid": "537048168",
            "v": "1.7.3",
            "platform": "10",
            "identifier": str(identifier),
            "usersig": str(usersig),
            "sdkappid": "1400401893",
            "accounttype": str(int(random.random()*100000000)),
            "contentType": "json",
            "apn": "1",
            "reqtime": str(time.time())[0:14]
        }
        response = session.get(self.a2_url, headers=self.headers, params=params)
        A2Key = json.loads(response.text).get("A2Key")
        TinyId = json.loads(response.text).get("TinyId")
        return A2Key, TinyId

    def get_imurl(self):
        data = {
            "businessKey": "im.key.shop.chat.servicepage",
            "projectName": "shop",
            "fromType": "1",
            "channelType": "5",
            "toUserId": "20217902",
            "toType": "2",
            "osType": "1",
            "consultType": "1",
            "bizType": "1",
            "bizId": "1428613",
            "sourceType": "3"
        }
        response = session.post(self.im_url, headers=self.headers, data=data)
        return json.loads(response.text).get("data").get("imUrl").split("?")[0]

    def get_openid(self, imUrl):
        params = {
            "t": str(time.time() * 1000),
            "isDingpa": "1"
        }
        respons = session.get(imUrl, headers=self.headers, params=params)
        return json.loads(respons.text).get("data")

    def get_code(self, token):
        params = {
            "token": str(token)
        }
        response = session.get(self.code_url, headers=self.headers, params=params)
        saveImage(response.content, "./code.jpg")
        showImage("./code.jpg")

    def get_longpollingid(self, a2, tinyid):
        params = {
            "websdkappid": "537048168",
            "v": "1.7.3",
            "platform": "10",
            "a2": str(a2),
            "tinyid": str(tinyid),
            "sdkappid": "1400401893",
            "contentType": "json",
            "accounttype": str(int(random.random()*100000000)),
            "apn": "1",
            "reqtime": str(int(time.time()))[0:14]
        }
        response = session.get(self.gpoll_url, headers=self.headers, params=params)
        return json.loads(response.text).get("LongPollingId")

    def get_eventarray(self, a2, tinyid, lpi):
        params = {
            "websdkappid": "537048168",
            "v": "1.7.3",
            "platform": "10",
            "a2": str(a2),
            "tinyid": str(tinyid),
            "sdkappid": "1400401893",
            "contentType": "json",
            "accounttype": str(int(random.random() * 100000000)),
            "apn": "1",
            "reqtime": str(int(time.time()))[0:14]
        }
        data = {"Cookie":{"NotifySeq":0,"NoticeSeq":0,"LongPollingId":lpi}}
        response = session.post(self.poll_url, headers=self.headers, params=params, data=data)
        print(response.text)

    def login(self, token):
        params = {
            "ttt": str(int(time.time() * 1000)),
            "token": str(token),
            "flag": "1",
            "src": "1"
        }
        while True:
            time.sleep(1)
            response = session.get(self.login_url, headers=self.headers, params=params)
            flag_dict = json.loads(response.text)
            if flag_dict.get("code") != 0:
                break
        removeImage("./code.jpg")

    def check_ok(self):
        if session.cookies.get("nickname"):
            print("登陆成功！当前账号为:" + session.cookies.get("nickname"))
        else:
            print("登陆失败！未知错误！")

    def send_msg(self, msg, a2, tinyid, openid, data_dict, msgseq, msgrandom, msgtimestamp):
        params = {
            "websdkappid": "537048168",
            "v": "1.7.3",
            "platform": "10",
            "a2": str(a2),
            "tinyid": str(tinyid),
            "sdkappid": "1400401893",
            "contentType": "json",
            "apn": "1",
            "reqtime": str(int(time.time()*1000)),
            "tjg_id": tinyid + "-" + str(data_dict.get("talkId"))
        }
        data = {
            "From_Account":openid,
            "To_Account":data_dict.get("openId"),
            "MsgTimeStamp":msgtimestamp,
            "MsgSeq":msgseq,
            "MsgRandom":msgrandom,
            "MsgBody":[{
                "MsgType":"TIMTextElem",
                "MsgContent":{"Text":msg}
            }]
        }
        data = json.dumps(data)
        response = session.post(self.sendmsg, data=data, headers=self.headers, params=params)
        if json.loads(response.text).get("ActionStatus") == "OK":
            print("已将<%s>发送出去！" % msg)
        else:
            print("发送失败！")
            print(response.text)

    def get_Msg(self, a2, tinyid, data_dict, openId):
        url = "https://webim.tim.qq.com/v4/openim/getroammsg"
        params = {
            "platform": "10",
            "a2": a2,
            "tinyid": tinyid,
            "sdkappid": "1400401893",
            "contentType": "json",
            "apn": "1",
            "websdkappid": "537048168",
            "v": "1.7.3",
            "reqtime": str(int(time.time()*1000))
        }
        data = {"Peer_Account":data_dict.get("openId"),"MaxCnt":20,"LastMsgTime":0,"MsgKey":"","WithRecalledMsg":1}
        data = json.dumps(data)
        response = session.post(url, headers=self.headers, params=params, data=data)
        MsgSeq = None
        MsgRandom = None
        MsgTimeStamp = None
        pos = -1
        for i in range(len(json.loads(response.text).get("MsgList"))):
            try:
                if json.loads(response.text).get("MsgList")[pos].get("From_Account") == openId:
                    MsgSeq = json.loads(response.text).get("MsgList")[pos].get("MsgSeq")
                    MsgRandom = json.loads(response.text).get("MsgList")[pos].get("MsgRandom")
                    MsgTimeStamp = json.loads(response.text).get("MsgList")[pos].get("MsgTimeStamp")
                    break
                pos -= 1
            except:
                MsgSeq = 5000000000
                MsgRandom = int(random.random() * 10 ** 8)
                MsgTimeStamp = int(time.time())
        if (MsgSeq is None) or (MsgRandom is None) or (MsgTimeStamp is None):
            MsgSeq = 5000000000
            MsgRandom = int(random.random() * 10 ** 8)
            MsgTimeStamp = int(time.time())
        return MsgSeq, MsgRandom, MsgTimeStamp

    def run(self):
        token = self.get_token()
        self.get_code(token)
        self.login(token)
        self.check_ok()
        imUrl = self.get_imurl()
        usersig, identifier, openId = self.get_user_sign()
        A2Key, TinyId = self.get_a2(usersig, identifier)
        user_data = self.get_openid(imUrl)
        MsgSeq, MsgRandom, MsgTimeStamp = self.get_Msg(A2Key, TinyId, user_data, openId)
        print(MsgSeq, MsgRandom, MsgTimeStamp)
        msg = input("请输入要发送的内容:")
        self.send_msg(msg, A2Key, TinyId, openId, user_data, MsgSeq, MsgRandom, MsgTimeStamp)


def main():
    ZBJ = Zhubajie_Spider()
    ZBJ.run()


if __name__ == '__main__':
    main()