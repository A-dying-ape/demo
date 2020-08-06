# coding:utf-8
"""
获取请求信息的cookie值，放回一个可迭代的对象
"""
from urllib import request
from http import cookiejar

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}


def get_cookies(url):
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    opener.open(url)
    return cookie
