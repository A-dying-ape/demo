from util.request import request_url
from setting import HEADERS
from lxml import etree
from setting import HOMENAVMIN
from urllib import parse
import os
import re
import time
import random


class Module():
    def __init__(self):
        self.module_menu = "http://www.duoguan.com/"

    def get_menu(self):
        time.sleep(random.randint(1,2))
        response = request_url(url=self.module_menu, headers=HEADERS, method='get', proxy=True)
        html = etree.HTML(response.content.decode("utf-8"))
        div_list = html.xpath("//div[@class='ModuleMin']/div[position()>1]")
        for div in  div_list:
            for kind in div.xpath("./h3/text()"):
                if kind in HOMENAVMIN:
                    path = "./template/%s" %kind.strip()
                    try:
                        os.mkdir(path)
                    except:
                        print("%s文件已存在" % path)
                    if kind == "商家助手":
                        pass
                    else:
                        dd_list = div.xpath("//h3[text()='%s']/following-sibling::*[1]/dd" %kind)
                        self.get_module_info(dd_list, path)

    def get_module_info(self, ddl, path):
        path1 = path
        for dd in ddl:
            temp_dict = {}
            temp_list = list()
            text = dd.xpath("./a/text()")[0].strip()
            path2 = path1 + "/" + text
            try:
                os.mkdir(path2)
            except:
                print("%s文件已存在" % path2)
            href = dd.xpath("./a/@href")[0].strip()
            href = parse.urljoin(self.module_menu, href)
            time.sleep(random.randint(1, 2))
            response = request_url(url=href, headers=HEADERS, method='get', proxy=True)
            html = etree.HTML(response.content.decode("utf-8"))
            # 获取详情介绍
            try:
                temp_dict["详情描述"] = html.xpath("//div[@class='right']/p/text()")[0].strip()
            except:
                temp_dict["详情描述"] = ""
            try:
                temp_dict["应用场景"] = html.xpath("//div[@class='right']/div[1]/div[1]/span/text()")[0].strip()
            except:
                temp_dict["应用场景"] = ""
            try:
                temp_dict["模块搭配"] = html.xpath("//div[@class='right']/div[1]/div[2]/span/text()")[0].strip()
            except:
                temp_dict["模块搭配"] = ""
            # 用异常匹配所有的图片
            try:
                src_info = html.xpath("//div[@class='Details-info']/p[2]/span/img/@src")[0].strip()
            except:
                try:
                    src_info = html.xpath("//div[@class='Details-info']/p[last()]/span/img/@src")[0].strip()
                except:
                    try:
                        src_info = html.xpath("//div[@class='Details-info']/p[2]/img/@src")[0].strip()
                    except:
                        try:
                            src_info = html.xpath("//div[@class='Details-info']/p[last()]/img/@src")[0].strip()
                        except:
                            src_info = html.xpath("//div[@class='Details-info']/div[last()]/img/@src")[0].strip()
            src_info = parse.urljoin(self.module_menu, src_info)
            src_slider = html.xpath("//div[@class='swiper-container']/div[1]/div/a/@style")
            for src in src_slider:
                src = re.search("background-image: url\((.*)\)", src).group(1)
                src = parse.urljoin(self.module_menu, src)
                temp_list.append(src)
            self.save_msg(temp_dict, src_info, temp_list, path2)

    def save_msg(self, td, si, tl, path):
        # 保存详情信息
        with open(path + "/" + "info.txt", "w", encoding="utf-8") as f:
            f.write(str(td))
        # 保存详情图片
        time.sleep(0.5)
        iresponse = request_url(url=si, headers=HEADERS, method='get', proxy=True)
        with open(path + "/" + "info.png", "wb") as f:
            f.write(iresponse.content)
        # 保存轮播图片
        for src in tl:
            time.sleep(0.5)
            text = re.split("/", src)[-1]
            if (text == "") or (text is None):
                continue
            sresponse = request_url(url=src, headers=HEADERS, method='get', proxy=True)
            with open(path + "/" + text, "wb") as f:
                f.write(sresponse.content)

    def run(self):
        self.get_menu()