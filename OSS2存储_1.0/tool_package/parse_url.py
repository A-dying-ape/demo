from urllib.parse import urlunparse, urlparse


def merge_url(scheme="", netloc="", path="", params="", query="", fragment=""):
    """
    合并url地址
    :param scheme: 协议
    :param netloc: 服务器地址
    :param path: 路径
    :param params: 参数
    :param query: 查询部分
    :param fragment: 分片部分
    :return: url地址
    """
    return urlunparse([scheme, netloc, path, params, query, fragment])


def split_url(url):
    """
    解析url地址
    :param url: 解析的url
    :return: 返回一个可迭代对象
    """
    result = urlparse(url)
    return result