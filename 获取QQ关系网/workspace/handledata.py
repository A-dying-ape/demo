# coding:utf-8
"""
update: 2020/8/22 17:01:42
author: 一只快死的猿
"""
import re
import json
import time
from setting import HEADERS
from sqlpool.pool import ConnMysql


headers = HEADERS
conn = ConnMysql()


def judge_done(uin):
    """
    判断当前qq是否爬取过了
    :param uin: int
    :return: dict
    """
    sql = "select count(*) from qquser where uin=%s" % uin
    return conn.sql_select_one(sql)


def insert_qq(item):
    """
    把首次爬取得账号保存到数据库
    :param item: tuple
    :return: None
    """
    isql = "insert into qquser (uin, nick, break) values %s" % str(item)
    conn.sql_change_msg(isql)


def insert_saysay(item):
    """
    保存说说数据
    :param item: list
    :return: None
    """
    sql = "insert into qqsaysay (uin, saysay, img) values %s" % str(tuple(item))
    conn.sql_change_msg(sql)


def crack_unikey(msg, g_tk):
    """
    破解unikey重要参数
    :param msg: dict
    :param g_tk: str
    :return: dict
    """
    r = True if msg.get("pictotal") == 1 else False
    s = None
    c = None
    if (r):
        s = msg.get("pic")[0].get("unilikekey")
        c = msg.get("pic")[0].get("curlikekey")
    if msg.get("rt_tid") and msg.get("rt_nosrc"):
        key1 = "http://user.qzone.qq.com/119/mood/" + str(msg.get("rt_tid")) + "." + str(msg.get("rt_source"))
        key2 = "http://user.qzone.qq.com/" + str(msg.get("uin")) + "/mood/" + str(msg.get("tid")) + "." + str(
            msg.get("t1_source"))
    elif msg.get("rt_tid"):
        key1 = "http://user.qzone.qq.com/" + str(msg.get("rt_uin")) + "/mood/" + str(msg.get("rt_tid")) + "." + str(
            msg.get("rt_source"))
        key2 = "http://user.qzone.qq.com/" + str(msg.get("uin")) + "/mood/" + str(msg.get("tid")) + "." + str(
            msg.get("t1_source"))
    elif (r and (s or c)):
        key1 = s or c
        key2 = c or s
    else:
        key1 = "http://user.qzone.qq.com/" + str(msg.get("uin")) + "/mood/" + str(msg.get("tid")) + "." + str(
            msg.get("t1_source"))
        key2 = "http://user.qzone.qq.com/" + str(msg.get("uin")) + "/mood/" + str(msg.get("tid")) + "." + str(
            msg.get("t1_source"))
    params = {
        "_stp": str(time.time() * 1000),
        "unikey": key1 + key2,
        "face": "0<|>0<|>0<|>0<|>0<|>0<|>0<|>0<|>0<|>0",
        "fupdate": "1",
        "g_tk": g_tk
    }
    return params


def get_zan(session, params, queue):
    """
    获取点赞人的qq信息
    :param session: 登陆过后的session
    :param params: 请求参数
    :param queue: 队列
    :return: None
    """
    url = "https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/user/qz_opcnt2"
    res = session.get(url, headers=headers, verify=False, params=params)
    result = re.findall(r"_Callback\((.*)\);", res.text, re.S)
    result = json.loads(result[0])
    if result.get("data"):
        item = result.get("data")[0].get("current").get("likedata").get("list")
        if len(item) > 0:
            for i in item:
                query = judge_done(i[0])
                if query["count(*)"] == 0:
                    queue.put(i[0])


def get_comment_msg(msg, queue):
    """
    获取评论人的qq信息
    :param msg: dict
    :param queue: 队列
    :return: None
    """
    if msg.get("commentlist"):
        for i in msg.get("commentlist"):
            qq = i.get("uin")
            query = judge_done(qq)
            if query["count(*)"] == 0:
                queue.put(qq)


def get_rt_msg(msg, queue):
    """
    获取别转发人的qq信息
    :param msg: dict
    :param queue: 队列
    :return: None
    """
    if msg.get("rt_uin"):
        qq = msg.get("rt_uin")
        query = judge_done(qq)
        if query["count(*)"] == 0:
            queue.put(qq)


def get_saysay(result, g_tk, session, queue):
    """
    一个条说说爬虫总逻辑
    :param result: dict
    :param g_tk: str
    :param session: 登陆过后的session
    :param queue: 队列
    :return: None
    """
    for msg in result.get("msglist"):
        # 获取说说信息
        temp_list = []
        if msg.get("uin"):
            temp_list.append(msg.get("uin"))
        else:
            temp_list.append(0)
        if msg.get("rt_con"):
            temp_list.append(msg.get("rt_con").get("content"))
        else:
            temp_list.append(msg.get("content"))
        if msg.get("pic"):
            temp_pic = []
            for i in msg.get("pic"):
                if i.get("is_video"):
                    temp_pic.append(i.get("is_video"))
                else:
                    temp_pic.append(i.get("smallurl"))
            temp_list.append(str(temp_pic))
        else:
            temp_list.append("")
        insert_saysay(temp_list)
        # 获取点赞人的账号信息
        params = crack_unikey(msg, g_tk)
        get_zan(session, params, queue)
        # 获取评论人的账号信息
        get_comment_msg(msg, queue)
        # 获取被转发的账号信息
        get_rt_msg(msg, queue)


def start_saysay(g_tk, queue, session, proxy_ip):
    """
    一个账号爬虫总逻辑
    :param g_tk: str
    :param queue: 队列
    :param session: 登陆过后的session
    :param proxy_ip: 代理IP
    :return: None
    """
    say_url = "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6"
    session.proxies.update(proxy_ip)
    uin = queue.get()
    # query从源头上规避重复工作，提高性能
    query = judge_done(uin)
    # insert_flag避免一个qq多次查询数据库，提高性能
    insert_flag = True
    if query["count(*)"] == 0:
        pos = 0
        while True:
            sparams = {
                "uin": uin,
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "hostUin": uin,
                "ftype": "0",
                "sort": "0",
                "pos": str(pos),
                "num": "20",
                "replynum": "100",
                "callback": "_preloadCallback",
                "code_version": "1",
                "format": "jsonp",
                "need_private_comment": "1",
                "g_tk": g_tk
            }
            res = session.get(say_url, headers=headers, verify=False, params=sparams)
            result = None
            if re.findall(r"_Callback\((.*)\);", res.text, re.S):
                result = re.findall(r"_Callback\((.*)\);", res.text, re.S)
            elif re.findall(r"_preloadCallback\((.*)\);", res.text, re.S):
                result = re.findall(r"_preloadCallback\((.*)\);", res.text, re.S)
            else:
                print(res.text)
            result = json.loads(result[0])
            qq_name = result.get("usrinfo").get("name")
            if result.get("msglist") is None:
                if insert_flag:
                    item = (uin, qq_name, 0)
                    insert_qq(item)
                break
            else:
                pos += 20
                if insert_flag:
                    item = (uin, qq_name, 1)
                    insert_qq(item)
                    insert_flag = False
                get_saysay(result, g_tk, session, queue)
    else:
        pass
