# coding:utf-8


def get_cookies(cookies):
    cookies_dict = {}
    for item in cookies:
        cookies_dict[item.name] = item.value
    return cookies_dict
