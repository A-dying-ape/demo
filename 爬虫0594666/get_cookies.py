# coding:utf-8
from urllib import request
from http import cookiejar
import requests
import random


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}


def get_cookies(url, ip_pool):
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    opener.open(url)
    response = requests.get(url, proxies=random.choices(ip_pool)[0], headers=headers)
    return cookie, response.url