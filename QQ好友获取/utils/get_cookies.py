# coding:utf-8
from urllib import request
from http import cookiejar


def get_cookies(cookies):
    cookies_dict = {}
    for item in cookies:
        cookies_dict[item.name] = item.value
    return cookies_dict
