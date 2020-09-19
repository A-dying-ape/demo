import re


def deal_nbsp(response):
    return re.sub("&nbsp;", "", response.text)