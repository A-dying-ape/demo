# coding:utf-8
"""
构造url
"""
from urllib.parse import urlunparse, urlsplit


def parse_url(url, path, query, params="", fragment=""):
    res = urlsplit(url)
    return merge_url(str(res.scheme), str(res.netloc), str(path), str(params), str(query), str(fragment))


def merge_url(*args):
    url = urlunparse([i for i in args])
    return url
