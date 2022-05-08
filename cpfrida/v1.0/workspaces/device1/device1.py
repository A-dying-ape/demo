# !/usr/bin/env python
# coding=utf-8
# @Time    : 2022/04/20
# @Author  : XQE
# @Software: PyCharm


import os
import sys
import json
import config
sys.path.append("..")
from business import HandleBusiness


class Script(HandleBusiness):
    # script filename
    filename = str(os.path.basename(__file__).split(".")[0])

    def __init__(self):
        HandleBusiness.__init__(self, self.filename, os.path.join(config.project_path, "workspaces"))

    def hook_data(self):
        """
        hook the entrance
        """
        try:
            self.adapter_business()
        except Exception as e:
            self.logger.error("func hook data error:" + str(e), exc_info=True)
            if self.frida_object:
                self.frida_object.unload()
            self.logger.info("restart app ...")
            self.restart_app()
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
                self.handle_business()
            except Exception as e:
                self.logger.error("my_message_handler error:" + str(e), exc_info=True)
        else:
            self.logger.error("hook error:" + str(message), exc_info=False)
            if self.remove_monitor:
                self.logger.info("devices may be banned, remove the monitor option.")
                status = self.inform(self.handle_inform_text(**{"device": self.filename, "err_msg": str(message)}))
                self.logger.info("send inform %s ." % str(status))
                self.remove_monitor_conf()
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
                self.logger.info("reboot phone ...")
                self.reboot()
                self.logger.info("restart app ...")
                self.restart_app()
                self.frida_object = None


if __name__ == "__main__":
    Script().run()
