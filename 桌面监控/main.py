#! python3
# coding: utf-8
from workspace import SendAudioEmail, RecordAudio
import configparser
import os


# 获取录制配置
record_config = configparser.ConfigParser()
record_config.read("./conf/record_setting.conf", encoding='utf-8')
fps = record_config.get("CONFIG", "fps")

# 获取邮箱配置参数
email_config = configparser.ConfigParser()
email_config.read("./conf/email_setting.conf", encoding='utf-8')
from_addr = email_config.get("CONFIG", "from_addr")
to_addr = email_config.get("CONFIG", "to_addr")
subject = email_config.get("CONFIG", "subject")
type = email_config.get("CONFIG", "type")
authorization_code = email_config.get("CONFIG", "authorization_code")
smtp_server = email_config.get("CONFIG", "smtp_server")


def main():
    # 调用录屏接口
    ra = RecordAudio.RecordAudio(
        fps=fps
    )
    audio_name = ra.start_record()
    # 调用邮件接口
    sae = SendAudioEmail.SendAudioEmail(
        from_addr=from_addr,
        to_addr=to_addr,
        subject=subject,
        content_path=audio_name,
        type=type,
        authorization_code=authorization_code,
        smtp_server=smtp_server
    )
    sae.send_audio_email()
    os.remove(audio_name)


if __name__ == '__main__':
    while True:
        main()