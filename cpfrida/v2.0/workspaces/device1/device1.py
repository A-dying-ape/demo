# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import os
import sys
import time
import json
import config
import multiprocessing
sys.path.append("..")
from business import HandleBusiness


pool = None


def display_err_info(value):
    """
    when the business goes wrong
    :param value: error mark
    :return: None
    """
    global pool
    if value == "err":
        pool.terminate()


class Script(HandleBusiness):
    # script filename
    filename = str(os.path.basename(__file__).split(".")[0])

    def __init__(self, device, url):
        HandleBusiness.__init__(self, self.filename, device, url, os.path.join(config.project_path, "workspaces"))

    def hook_data(self):
        """
        hook the entrance
        """
        try:
            self.adapter_business()
        except Exception as e:
            self.logger.error("func hook data error:" + str(e), exc_info=False)
            if self.frida_object:
                self.frida_object.unload()
            self.frida_object = None

    def my_message_handler(self, message, payload):
        """
        send Data receiving function
        :param message: send data
        :param payload:
        """
        if message["type"] == "send":
            try:
                self.post_response = json.loads(message["payload"])
                print(message["payload"])
                self.handle_business()
            except Exception as e:
                self.logger.error("my_message_handler error:" + str(e), exc_info=False)
        else:
            self.logger.error("hook error:" + str(message), exc_info=False)
            if self.remove_monitor:
                self.logger.info("devices may be banned, remove the monitor option.")
                status = self.inform(self.handle_inform_text(**{"device": self.filename, "err_msg": str(message)}))
                self.logger.info("send inform %s ." % str(status))
                self.remove_monitor_conf()
                return "err"
            else:
                if "token" in str(message) and os.path.exists(self.cookie_file):
                    os.remove(self.cookie_file)
                    self.vx_cookie = None
                    self.logger.info("the cookie has expired. obtain it again.")
                else:
                    self.remove_monitor = True

    def run(self):
        """
        single program entry
        """
        self.logger.info("=============== start hook script ===============")
        while True:
            try:
                self.hook_data()
            except Exception as e:
                self.logger.error("script run fail: " + str(e), exc_info=False)
                self.frida_object = None


def start_work(business, url):
    """
    begin
    :param business: business nickname
    :param url: hook parameter address
    :return: None
    """
    Script(business, url).run()


if __name__ == "__main__":
    # Script("detail", "http://172.23.10.70:8181/detail/8018/task?uuid={}&host={}").run()
    import os
    pool = multiprocessing.Pool(len(config.get_url))
    for business, url in config.get_url.items():
        pool.apply_async(func=start_work, args=(business, url), error_callback=display_err_info)
    pool.close()
    pool.join()