# coding:utf-8
"""
对目标服务器进行请求判断，如果返回的是错误的信息，则等待1s重新请求，共请求3次
"""
import requests
import random
from retrying import retry


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def _parse_url(url, headers, proxies_list, verify, method):
    if method == "GET":
        response = requests.get(url, headers=headers, proxies=random.choices(proxies_list)[0], verify=verify)
    else:
        response = requests.post(url, headers=headers, proxies=random.choices(proxies_list)[0], timeout=5)
    # 响应返回状态必须是200，而且不为空内容，为空重新请求一次
    assert response.status_code == 200
    try:
        assert response.text != ""
    except:
        response = requests.get(url, headers=headers, proxies=random.choices(proxies_list)[0], timeout=5)
    assert response.status_code == 200
    return response


def request_url(url, headers, proxies_list, verify=False, method="GET"):
    try:
        html = _parse_url(url, headers, proxies_list, verify, method)
    except:
        html = None
    return html
