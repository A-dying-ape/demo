import time
import requests
import parsel
import multiprocessing
from monitor import Monitor


class HandleAlarm(Monitor):
    """
    微信视频号专用监控
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

    def __init__(self, url):
        """
        初始化环境
        :param url: 监控页面
        """
        Monitor.__init__(self)
        self.url = url

    def spider(self):
        """
        获取监控页面
        :return 监控页面
        """
        response = requests.get(self.url, headers=self.headers)
        return response.text

    @staticmethod
    def handle_content(text):
        """
        处理监控页面信息
        :param text: 页面信息
        :return: 所有设备信息  list
        """
        selector = parsel.Selector(text)
        tr_list = selector.xpath("/html/body/div[2]/table/tbody/tr")
        tmp_list = list()
        for tr in tr_list:
            tmp_dict = dict()
            tmp_dict["序号"] = tr.xpath("./td[1]/text()").get()
            tmp_dict["设备Id"] = tr.xpath("./td[2]/span/text()").get()
            tmp_dict["状态"] = tr.xpath("./td[2]/span/@style").get()
            tmp_dict["设备名称"] = tr.xpath("./td[3]/input/@value").get()
            tmp_dict["IP"] = tr.xpath("./td[4]/text()").get()
            tmp_dict["是否限制"] = tr.xpath("./td[5]/text()").get()
            tmp_dict["最后回调时间"] = tr.xpath("./td[6]/text()").get()
            tmp_dict["统计时间"] = tr.xpath("./td[7]/text()").get()
            tmp_dict["每日的次数"] = tr.xpath("./td[8]/text()").get()
            tmp_dict["总次数"] = tr.xpath("./td[9]/text()").get()
            tmp_list.append(tmp_dict)
        return tmp_list

    def analyse(self, data):
        """
        分析当前设备是否正常
        :param data: 设备信息
        :return: 异常设备列表  list
        """
        handle_devices_list = list()
        for d in data:
            int_time = int(time.mktime(time.strptime(d.get("最后回调时间").replace("/", "-"), '%Y-%m-%d %H:%M:%S')))
            time_diff = int(time.time()) - int_time
            if (d.get("状态") is not None) and (time_diff > int(self.monitor_conf['config']['reboot'])) and (d.get("设备名称") in self.monitor_conf.options("devices")):
                handle_devices_list.append(d.get("设备名称"))
        return handle_devices_list

    def run(self):
        """
        异常设备分析和进程维护主逻辑
        :return:需要重启的进程  list
        """
        cmd_start_list = None
        try:
            self.logger.info("=============== start monitoring ===============")
            local_err_process = self.check_local_pro()
            context = self.spider()
            devices_info = self.handle_content(context)
            handle_list = self.analyse(devices_info)
            devices_list = self.check_telnet(list(set(local_err_process + handle_list)))
            cmd_start_list = self.handle_devices(devices_list)
            self.logger.info("=============== end monitoring ===============")
        except Exception as e:
            self.logger.error("script error: " + str(e), exc_info=False)
        return cmd_start_list


if __name__ == '__main__':
    url = "http://www.baidu.com"
    ha = HandleAlarm(url)
    try:
        cmd_start_list = ha.run()
        for cmd in cmd_start_list:
            multiprocessing.Process(target=ha.restart_process, args=(cmd,)).start()
        ha.logger.info(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + " -- :" + "巡查完一轮设备!")
    except Exception as e:
        ha.logger.error(str(e))
