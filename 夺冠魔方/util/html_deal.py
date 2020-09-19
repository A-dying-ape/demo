import re


def html_deal(response):
    return re.sub("&nbsp;", "", response.text)