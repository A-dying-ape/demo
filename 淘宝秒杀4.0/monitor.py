import time
import json
import requests
import random
import spike_goods


def check_cookie():
    count = 0
    temp_list = []
    with open("taobao_cookies.txt", "r") as f:
        while True:
            cookie = f.readline()
            if cookie:
                count += 1
                temp_list.append(eval(cookie))
            else:
                break
    return temp_list, count


def str_to_timestamp(str_time):
    format = '%Y-%m-%d %H:%M:%S'
    time_tuple = time.strptime(str_time, format)
    result = time.mktime(time_tuple)
    return int(result)


def monitor_page(url, mtime, updata_log, cookie_list, proxy_flag, spike_count):
    begin_time = str_to_timestamp(mtime)
    ip_pool = None
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    }
    if proxy_flag:
        with open("ip_pool", "r") as f:
            ip_pool = f.read()
        ip_pool = json.loads(ip_pool)
        proxy_ip = {"http": random.choices(ip_pool)}
        page_source = requests.get(url, headers=headers, proxies=proxy_ip).text
    else:
        page_source = requests.get(url, headers=headers).text
    while True:
        if begin_time <= int(time.time()):
            updata_log.emit("-"*10 + "开始秒杀" + "-"*10)
            flag = spike_goods.run(url, ip_pool, cookie_list, page_source, updata_log, proxy_flag, spike_count)
            if flag:
                break
        else:
            updata_log.emit(">>等待秒杀时间到来！")


def run_login(url, mtime, updata_log, proxy_flag, spike_count):
    cookie_list, count = check_cookie()
    if count > 0:
        monitor_page(url, mtime, updata_log, cookie_list, proxy_flag, spike_count)
    else:
        updata_log.emit(">>读取的cookie缓存为空，请清除cookie后重新登录！")
        return