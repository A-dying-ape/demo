# coding:utf-8
import re
import random
import time
import json
import threading
import pymysql
import queue
from lxml import etree
from urllib import parse
from retryl_request import request_url
from by_img_spiders import By_Img_Spiders


class By_Anfuweb_Spiders():

    def __init__(self, ippool):
        self.start_url = "http://00594666.com/"
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        self.conn = pymysql.connect(host="", port=, user="", password="", database="", charset="")
        self.crs = self.conn.cursor()
        self.ip_pool = ippool
        self.q = queue.Queue()

    def nav_url_spider(self):
        response = request_url(self.start_url, headers=self.index_headers, proxies_list=self.ip_pool)
        if response is None:
            print("请求首页失败！")
        nav_html = etree.HTML(response.text)
        nav_href = nav_html.xpath("//div[@class='category']/div/h3/a/@href")
        nav_href = [parse.urljoin(self.start_url, href) for href in nav_href]
        nav_kind = nav_html.xpath("//div[@class='category']/div/h3/a/text()")
        for i in range(0, len(nav_kind)):
            kind_insert = """insert into store_kind (kind_name, kind_href) values ('%s', '%s') on duplicate key update kind_name = '%s';""" % (
            nav_kind[i], nav_href[i], nav_kind[i])
            try:
                self.crs.execute(kind_insert)
            except:
                self.conn.ping()
                self.crs = self.conn.cursor()
                self.crs.execute(kind_insert)
            self.conn.commit()
        self.crs.execute("select * from store_kind")
        return [(kind[0], kind[2]) for kind in self.crs.fetchall()]

    def store_url_spider(self, kind_id, kind_url, temp_list=None):
        if temp_list is None:
            temp_list = list()
        response = request_url(kind_url, headers=self.index_headers, proxies_list=self.ip_pool)
        if response is None:
            print("页面请求失败：" + kind_url)
        html = etree.HTML(response.text)
        store_html = html.xpath("//div[@class='def_border hot_tj_index c_page']/div[@class='data']/ul/li/a[last()]/@href")
        for store_href in store_html:
            temp_list.append(parse.urljoin(self.start_url, store_href))
        next_page = html.xpath("//div[@class='pagination'][1]/a[text()='下一页']/@href")
        if len(next_page) <= 0:
            return self.get_store_info(temp_list, kind_id)
        else:
            self.store_url_spider(kind_id, parse.urljoin(kind_url, next_page[0]), temp_list)

    def get_store_info(self, store_href_list, kind_id):
        for store_href in store_href_list:
            # time.sleep(random.randint(2, 4))
            response = request_url(store_href, headers=self.index_headers, proxies_list=ip_pool)
            if response is None:
                print("页面请求失败：" + store_href)
            else:
                try:
                    html = etree.HTML(response.text)
                except:
                    with open("./test1/" + store_href[-6:-11:-1], "w", encoding="utf-8") as f:
                        f.write(response.text)
                dl_list = html.xpath("//div[@class='rows']/dl")
                temp_dict = {"kind_id": kind_id, "store_href": store_href}
                for dl in dl_list:
                    a = dl.xpath("./dt/text()")[0].strip()
                    b = dl.xpath("./dd")[0]
                    if a == "商家信誉：":
                        try:
                            temp_dict["credit_count"] = re.findall(r'\d', str(b.xpath("./img/@src")[0]))[0] + "星"
                        except:
                            temp_dict["credit_count"] = "6星"
                    elif a == "店名：":
                        try:
                            temp_dict["store_name"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["store_name"] = ""
                    elif a == "网址(1)：":
                        try:
                            temp_dict["albums_url1"] = b.xpath("./a/@href")[0].strip()
                        except:
                            temp_dict["albums_url1"] = ""
                    elif a == "网址(2)：":
                        try:
                            temp_dict["albums_url2"] = b.xpath("./a/@href")[0].strip()
                        except:
                            temp_dict["albums_url2"] = ""
                    elif a == "搜福一下：":
                        try:
                            temp_dict["soufu_url"] = b.xpath("./a/@href")[0].strip()
                        except:
                            temp_dict["soufu_url"] = ""
                    elif a == "QQ(1)：":
                        try:
                            temp_dict["QQ1"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["QQ1"] = ""
                    elif a == "QQ(2)：":
                        try:
                            temp_dict["QQ2"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["QQ2"] = ""
                    elif a == "微信：":
                        try:
                            temp_dict["wechart"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["wechart"] = ""
                    elif a == "电话：":
                        try:
                            temp_dict["phone"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["phone"] = ""
                    elif a == "地址：":
                        try:
                            temp_dict["address"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["address"] = ""
                    elif a == "主营产品：":
                        try:
                            temp_dict["product"] = b.xpath("./text()")[0].strip()
                        except:
                            temp_dict["product"] = ""
                    elif a == "扫一扫：":
                        try:
                            temp_dict["wechart_code"] = parse.urljoin(self.start_url, b.xpath("./img/@src")[0].strip())
                        except:
                            temp_dict["wechart_code"] = ""
                    else:
                        print("未知的条栏：" + store_href)
                temp_str = ""
                for i in tuple(" %s = '%s', " % (k, v) for k, v in temp_dict.items()):
                    temp_str += i
                store_insert = "insert into store %s values %s on duplicate key update %s;" % (re.sub(r"'", "", str(tuple(temp_dict))), str(tuple(temp_dict.values())), temp_str[0:-2])
                self.q.put(store_insert)

    def save_store_info(self):
        end_flag = 0
        while True:
            if self.q.empty():
                if end_flag >= 20:
                    break
                end_flag += 1
                time.sleep(random.randint(1, 2))
            else:
                end_flag = 0
                store_insert = self.q.get()
                print(store_insert)
                try:
                    self.crs.execute(store_insert)
                except:
                    self.conn.ping()
                    self.crs = self.conn.cursor()
                    self.crs.execute(store_insert)
                self.conn.commit()

    def __del__(self):
        print("-"*50 + "爬虫完成" + "-"*50)
        self.crs.close()
        self.conn.close()

    def run(self):
        nav_kind_list = self.nav_url_spider()
        thread_list = list()
        thread_list.append(threading.Thread(target=self.save_store_info))
        for nav_kind in nav_kind_list:
            thread_list.append(threading.Thread(target=self.store_url_spider, args=(nav_kind[0], nav_kind[1])))
        for t in thread_list:
            t.start()
        # By_Img_Spiders(self.ip_pool, self.conn, self.crs).run()


if __name__ == '__main__':
    with open("./ip_pool", "r") as f:
        content = f.read()
    ip_pool = json.loads(content)
    bas = By_Anfuweb_Spiders(ip_pool)
    bas.run()
