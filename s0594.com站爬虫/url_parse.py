from urllib.parse import urlunparse, urlsplit


def parse_url(url, path, query, params="", fragment=""):
    res = urlsplit(url)
    return merge_url(res.scheme, res.netloc, path, params, query, fragment)


def merge_url(*args):
    res = urlunparse([i for i in args])
    return res