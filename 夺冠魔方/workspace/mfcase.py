from util.request import request_url
from setting import HEADERS, MFCASENAV
from lxml import etree
from urllib import parse
import os
import re
import time
import random


class Mfcase():
    def __init__(self):
        self.parse_url = "http://www.duoguan.com/"
        self.mfcase_index = "http://www.duoguan.com/mfcase/"

    def get_top_nav(self):
        time.sleep(random.randint(1,2))
        response = request_url(url=self.mfcase_index, headers=HEADERS, method='get', proxy=True)
        html = etree.HTML(response.content.decode("utf-8"))
        for i in html.xpath("//div[@class='casebox']/div[1]/a/text()"):
            if i.strip() in MFCASENAV:
                path = "./case/" + i.strip()
                try:
                    os.mkdir(path)
                except:
                    print("%s文件已存在" % path)
                href = html.xpath("//div[@class='casebox']/div[1]/a[text()='%s']/@href" %i)[0].strip()
                href = parse.urljoin(self.parse_url, href)
                self.get_kind_nav(path, href)

    def get_kind_nav(self, path ,href):
        time.sleep(random.randint(1,2))
        response = request_url(url=href, headers=HEADERS, method='get', proxy=True)
        html = etree.HTML(response.content.decode("utf-8"))
        if html.xpath("//div[@class='caseSubNav']"):
            a_list = html.xpath("//div[@class='caseSubNav']/div/a")[1:]
            for a in a_list:
                text = re.sub("\(\d{1,3}\)", "", a.xpath("./text()")[0].strip())
                kpath = path + "/" + text
                try:
                    os.mkdir(kpath)
                except:
                    print("%s文件已存在" % kpath)
                url = "http://www.duoguan.com/e/tags/?tagname=" + text
                self.get_info(kpath, url)
        else:
            self.get_info(path, href)

    def get_info(self, path, url):
        time.sleep(1)
        response = request_url(url=url, headers=HEADERS, method='get', proxy=True)
        html = etree.HTML(response.content.decode("utf-8"))
        li_list = html.xpath("//ul[@class='clearfix caselist']/li")
        for li in li_list:
            src = parse.urljoin(self.parse_url, li.xpath("./div[@class='casema']/img/@src")[0].strip())
            text = li.xpath("./div[@class='p15']/h2/text()")[0].strip()
            time.sleep(0.5)
            sresponse = request_url(url=src, headers=HEADERS, method='get', proxy=True)
            with open(path + "/" + text + ".jpg", "wb") as f:
                f.write(sresponse.content)

    def run(self):
        self.get_top_nav()