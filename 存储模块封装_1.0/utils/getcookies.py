# coding:utf-8
from urllib import request
from http import cookiejar


def ucookies(url):
    """
    获取请求的cookie
    :param url: 请求地址
    :return: ccookie进一步处理
    """
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    opener.open(url)
    return ccookies(cookie)


def ccookies(cookies):
    """
    处理cookie
    :return:
    :param cookies: cookie可迭代对象
    :return: 字典k:cookies.name,v:cookies.value
    """
    cookies_dict = {}
    for item in cookies:
        cookies_dict[item.name] = item.value
    return cookies_dict
