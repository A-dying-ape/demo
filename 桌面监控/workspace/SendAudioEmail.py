# coding: utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.header import Header


class SendAudioEmail():
    def __init__(self, **kwargs):
        # 发信方
        self.from_addr = kwargs.get("from_addr")
        # 收信方
        self.to_addr = kwargs.get("to_addr")
        # 邮件主题
        self.subject = kwargs.get("subject")
        # 发送音频内容
        self.content_path = kwargs.get("content_path")
        # 内容类型  文本text,图片image,音频audio,应用程序application
        self.type = kwargs.get("type")
        # 授权码
        self.authorization_code =  kwargs.get("authorization_code")
        # 发信服务器
        self.smtp_server = kwargs.get("smtp_server")

    def _create_header(self, msg):
        # 构造邮件请求头
        msg['From'] = Header(self.from_addr)
        msg['To'] = Header(self.to_addr)
        msg['Subject'] = Header(self.subject)

    def _conn_server(self):
        # 开启发信服务，使用的是加密传输
        if self.smtp_server == "smtp.qq.com":
            server = smtplib.SMTP_SSL()
            server.connect(self.smtp_server, 465)
        elif self.smtp_server == "smtp.163.com":
            server = smtplib.SMTP_SSL()
            server.connect(self.smtp_server, 25)
        else:
            print("未匹配发信服务器类型！")
            server = None
        # 登录发信邮箱
        try:
            server.login(self.from_addr, self.authorization_code)
        except Exception as e:
            print('%s' % e)
        return server

    def send_audio_email(self):
        # 区别邮件内容,分别构造正文
        if self.type == "text":
            with open(self.content_path, "rb") as f:
                msg = MIMEText(f.read(), 'plain')
        elif self.type == "image":
            with open(self.content_path, "rb") as f:
                msg = MIMEImage(f.read(), 'plain')
        elif self.type == "audio":
            with open(self.content_path, "rb") as f:
                msg = MIMEAudio(f.read(), 'plain')
        elif self.type == "application":
            with open(self.content_path, "rb") as f:
                msg = MIMEApplication(f.read(), 'plain')
        elif self.type == None:
            with open(self.content_path, "rb") as f:
                msg = MIMEText(f.read(), 'plain')
        else:
            print("未识别文件类型！")
            msg = None
        self._create_header(msg)
        server = self._conn_server()
        # 发送邮件
        server.sendmail(self.from_addr, self.to_addr, msg.as_string())
        print("已发送")
        self._close_conn(server)

    def _close_conn(self, server):
        # 关闭服务
        server.quit()
