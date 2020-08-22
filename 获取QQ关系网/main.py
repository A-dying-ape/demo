# coding:utf-8
"""
update: 2020/8/22 17:01:42
author: 一只快死的猿
"""
import time
import random
import requests
import warnings
from workspace import handledata
from workspace.login import QQZone
from setting import IP_POOL
from sqlpool.pool import ConnMysql
from multiprocessing import Manager, Pool
from setting import HEADERS, PROCESSES, QUEUE_MAX_SIZE, WAIT_TIME, END_FLAG


warnings.filterwarnings('ignore')
session = requests.Session()
headers = HEADERS
conn = ConnMysql()
end_flag = 0


def qq_login():
    """
    用session登陆QQ空间获取个g_tk
    :return: g_tk : str
    """
    proxy_ip = random.choice(IP_POOL)
    qz = QQZone(session=session, proxies=proxy_ip)
    return qz.run()


def get_qq_account():
    """
    从数据库读取所有的QQ账号
    :return: list
    """
    sql = "select QQ1,QQ2 from store;"
    qqs = conn.sql_select_many(sql)
    qq_list = []
    for qq in qqs:
        if qq.get("QQ1"):
            qq_list.append(qq.get("QQ1").strip())
        elif qq.get("QQ2"):
            qq_list.append(qq.get("QQ2").strip())
    conn.release()
    return qq_list


if __name__ == '__main__':
    """
    程序总逻辑:
    一个账号一个子进程，
    利用进程池的特点避免后续裂变式开启进程，预防高并发使机器宕机。
    """
    g_tk = qq_login()
    qq_list = get_qq_account()
    """创建进程池爬取数据"""
    manager = Manager()
    queue = manager.Queue(QUEUE_MAX_SIZE)
    pool = Pool(processes=PROCESSES)
    for qq in qq_list:
        queue.put(qq)
    time.sleep(1)
    while True:
        if queue.empty():
            time.sleep(WAIT_TIME)
            end_flag += 1
            if end_flag >= END_FLAG:
                print("*"*20 + "已获取所有的QQ关系网！" + "*"*20)
                break
        else:
            end_flag = 0
            proxy_ip = random.choice(IP_POOL)
            pool.apply_async(handledata.start_saysay, (g_tk, queue, session, proxy_ip))
    pool.close()
    pool.join()
    print(queue.qsize())