# coding:utf-8
import requests
import re
import time
import random
import json
import sys
import threading
import get_cookies
import pymysql
import queue
import warnings
from lxml import etree
from urllib import parse
from retryl_request import request_url
from url_parse import parse_url


sys.setrecursionlimit(10000)
warnings.filterwarnings('ignore')


class By_Img_Spiders():

    def __init__(self, ip_pool):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        self.server_url = "service/album/get_album_themes_list.jsp"
        self.ip_pool = ip_pool
        self.conn = pymysql.connect(host="", port=, user="", password="",
                                    database="", charset="")
        self.crs = self.conn.cursor()
        self.cut_rule = 100
        self.q = queue.Queue()

    def select_from_store(self):
        """
        查询店铺信息，对对应的相册进行构造列表
        :return: final_temp_list 构造的列表结构[[store_id,albums1,albums2]]
        """
        try:
            self.crs.execute("select * from store;")
        except:
            self.conn.ping()
            self.crs = self.conn.cursor()
            self.crs.execute("select * from store;")
        final_temp_list = list()
        for store in self.crs.fetchall():
            temp_list = list()
            temp_list.append(store[0])
            if store[5] is not None:
                temp_list.append(store[5])
            if store[6] is not None:
                temp_list.append(store[6])
            final_temp_list.append(temp_list)
        return final_temp_list

    def select_url(self, store_list):
        """
        对商店的相册进行筛选过滤
        :param store_list: 商铺的信息列表
        :return: None
        """
        for msg_list in store_list:
            for url in msg_list[1:len(msg_list)]:
                if "yupoo.com" in url:
                    if url.startswith("http://") or url.startswith("https://"):
                        self.yupoo_url_handl(url, msg_list[0])
                    elif not url.startswith("http:") or url.startswith("https:"):
                        url = "http://" + url
                        self.yupoo_url_handl(url, msg_list[0])
                    elif (url.startswith("http:") or url.startswith("https:")) and (
                            not url.split(":")[1].startswith("//")):
                        url = url.split(":")[0] + "://" + url.split(":")[1]
                        self.yupoo_url_handl(url, msg_list[0])
                elif "w.url.cn" in url:
                    if url.startswith("http"):
                        self.other_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                elif "suo.im" in url:
                    if url.startswith("http"):
                        self.other_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                elif "szwego.com" in url:
                    if url.startswith("http"):
                        self.other_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                else:
                    pass
                    # self.err_url_handl(url, msg_list[0])

    def yupoo_url_handl(self, old_url, store_id):
        """
        对商铺的地址进行处理，构造定位地址，把相册请求地址定位在相册栏，并对被冻结的用户进行过滤
        :param old_url: 商铺的相册地址
        :param store_id: 商铺ID
        :return: None
        """
        response = request_url(old_url, headers=self.headers, proxies_list=self.ip_pool, )
        if response.status_code is not None:
            html = etree.HTML(response.text)
            try:
                albums_url = html.xpath("//div[@class='showheader__menus']/a[2]/@href")[0]
            except:
                try:
                    if len(re.findall("http|https", old_url)) == 2:
                        res = re.split(r"https", old_url)
                        for url in res:
                            self.yupoo_url_handl("http" + url, store_id)
                    elif not old_url.endswith("albums"):
                        old_url = re.search(r"http.*/albums", old_url).group()
                        self.yupoo_url_handl(old_url, store_id)
                except:
                    print("账户被冻结:" + old_url)
            else:
                new_url = parse.urljoin(response.url, albums_url)
                self.yupoo_spider(new_url, store_id)

    def other_url_handl(self, url, store_id):
        """
        获取shop_id，构造json信息的地址，对请求头进行初步处理
        :param url: 首页地址
        :param store_id: 商店ID
        :return: None
        """
        other_headers = None
        response = request_url(url, headers=self.headers, proxies_list=self.ip_pool)
        # 对于请求错误的url进行重新请求，直到正确
        if "b.oijgvrq.cn" in response.url:
            self.other_url_handl(url, store_id)
        # 从首页重定向的url中获取商品的id用于后面构造url
        try:
            shop_id = re.search(r"/shop_detail/(\w\d+)", response.url).group(1)
        except:
            print(response.url)
        else:
            if response is not None:
                cookies = get_cookies.get_cookies(url)
                url = parse_url(response.url.lower(), self.server_url, "")
                # 对请求头进行处理，获取请求首页时服务器设置的cookie值中的token字段构造请求头
                for item in cookies:
                    other_headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                        "cookie": "%s=%s" % (item.name, item.value)
                    }
                # 对于一些特殊的商店因为请求头中服务器没有设置token字段，所有手动构造
                if "token" not in other_headers["cookie"]:
                    other_headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                        "cookie": "token=Mzk4MDk3Q0E5RTZCN0I1MkYwMTYwNDlCQUNFNkQ5QzVFOEZCOTI1OEEwOTA2MDc0QzUzRTVCNDVDMTg1RTgzRTZBNTY1MTZDQTNFNDFCRkI2ODZGRTgxRjQxRDU3MEZD;"
                    }
                self.get_other_msg(other_headers, url, store_id, shop_id)

    def err_url_handl(self, url, store_id):
        """
        对异常和太特殊的url进行处理，如果后面需要扩展，可以从这里入手
        :param url: 一些错误的地址以及新的电商网站
        :param store_id: 商铺ID
        :return: None
        """
        if len(url) > 0:
            if url.startswith("http"):
                response = request_url(url, headers=self.headers, proxies_list=self.ip_pool)
                if response.status_code is not None:
                    pass
                else:
                    print("无效网址" + url)
            elif u'\u4e00' <= url <= u'\u9fff':
                pass
            else:
                url = "http://" + url
                response = request_url(url, headers=self.headers, proxies_list=self.ip_pool)
                if response.status_code is not None:
                    pass

    def yupoo_spider(self, yupoo_url, store_id):
        """
        用递归函数对定位在相册栏的页面进行翻页循环获取，而对获取的每一个相册对象传递给
        get_ypimg_page方法进行获取信息，递归结束的标志在‘后一页‘没有翻页连接
        :param yupoo_url:
        :param store_id:
        :return: None
        """
        response = request_url(yupoo_url, headers=self.headers, proxies_list=self.ip_pool)
        try:
            html = etree.HTML(response.text)
        except:
            print("请求失败：" + yupoo_url)
        else:
            if len(re.findall(r"该用户主页暂时关闭", response.text)) > 0:
                print("该用户主页暂时关闭:" + yupoo_url)
            elif html.xpath("//a[@class='showheader__menuslink showheader__active']/text()")[0] == "相册":
                temp_albums_list = html.xpath("//div[@class='showindex__parent']/div/a/@href")
                for albums in temp_albums_list:
                    self.get_ypimg_page(parse.urljoin(response.url, albums), store_id)
                if len(html.xpath("//div[@class='none_select pagination__buttons']/a[@title='后一页']/@href")) == 0:
                    pass
                else:
                    next_page = html.xpath("//div[@class='none_select pagination__buttons']/a[@title='后一页']/@href")[0]
                    next_page = parse.urljoin(response.url, next_page)
                    self.yupoo_spider(next_page, store_id)
            else:
                print("未知错误：" + yupoo_url)

    def get_ypimg_page(self, albums_href, store_id):
        """
        获取每个相册的信息，并对数据进行清洗放入队列
        :param albums_href:
        :param store_id:
        :return: None
        """
        try:
            albums_href1 = albums_href + "&tab=min"
            response = request_url(albums_href1, headers=self.headers, proxies_list=self.ip_pool)
        except:
            response = request_url(albums_href, headers=self.headers, proxies_list=self.ip_pool)
        try:
            html = etree.HTML(response.text)
        except:
            print("请求失败：" + albums_href)
        else:
            albums_name = html.xpath("//div[@class='showalbumheader__gallerydec']/h2/span[1]/text()")[0]
            albums_name = re.sub("\"|'", "“", albums_name)
            albums_name = re.sub(r"\n|\\|\r|\t|\r\n|\n\r", "", albums_name)
            other_msg = html.xpath("//div[@class='showalbumheader__gallerydec']/div[1]/text()")
            other_msg = re.sub("\"|'", "“", str(other_msg))
            other_msg = re.sub(r"\n|\\|\r|\t|\r\n|\n\r", "", other_msg)
            imgs = html.xpath(
                "//div[@class='showalbum__parent showalbum__min min']/div[@class='showalbum__children image__main']/div[@class='image__imagewrap']/img/@src")
            if len(imgs) <= 0:
                imgs = html.xpath(
                    "//div[@class='showalbum__parent showalbum__nor nor']/div[@class='showalbum__children image__main']/div[@class='image__imagewrap']/img/@src")
                if len(imgs) <= 0:
                    imgs = html.xpath(
                        "//div[@class='showalbum__parent showalbum__max max']/div[@class='showalbum__children image__main']/div[@class='image__imagewrap']/img/@src")
            img_href = list()
            for img in imgs:
                img = "http:" + img
                img_href.append(img)
            img_href = str(img_href)
            albums_info = (albums_name, store_id, albums_href, img_href, str(other_msg))
            insert_albums = "insert into albums (albums_name,store_id,albums_href,img_url,other_msg) values %s on duplicate key update %s;" % (
                str(albums_info),
                """albums_name="%s",store_id=%s,albums_href="%s",img_url="%s",other_msg="%s" """ % albums_info)
            insert_albums = re.sub(r"\n|\\|\r|\t|\r\n|\n\r", "", insert_albums)
            self.q.put(insert_albums)

    def get_other_msg(self, other_headers, url, store_id, shop_id, page_num=1):
        """
        对请求头完善处理，获取json字符串中的信息进行清洗，并构造插入语句放入队列，对异常页面进行简单输出
        :param other_headers: 初步构造的请求头
        :param url: json信息地址
        :param store_id: 商铺ID
        :param shop_id: 商品ID
        :param page_num: 页码 = 1
        :return: None
        """
        params = {
            "page_index": page_num,
            "act": "single_album",
            "shop_id": shop_id,
            "time_stamp": int(time.time() * 1000),
        }
        try:
            response = requests.get(url, params=params, proxies=random.choices(self.ip_pool)[0], headers=other_headers, timeout=5)
        except:
            print("连接失败：" + url)
        else:
            if "szwego.com" in response.url:
                if json.loads(response.text)['errcode'] == 0:
                    img_dict = json.loads(response.text)['result']['goods_list']
                    if len(img_dict) <= 0:
                        return
                    else:
                        page_num += 1
                        for img in img_dict:
                            temp_dict = dict()
                            temp_dict["img_url"] = str(img['imgs'])
                            temp_dict["albums_name"] = re.sub("\"|'", "“", img['title'])
                            temp_dict["albums_name"] = re.sub(r"\n|\\|\r|\t|\r\n|\n\r", "", temp_dict["albums_name"])
                            temp_dict["store_id"] = store_id
                            temp_dict["albums_href"] = img["link"]
                            temp_dict["other_msg"] = str(
                                "店铺:" + re.sub("\"|'", "“", img["shop_name"]) + ",上架时间：" + img["old_time"])
                            temp_str = ""
                            for i in tuple('%s = "%s",' % (k, v) for k, v in temp_dict.items()):
                                temp_str += i
                            temp_str = temp_str[0:-2] + "\""
                            insert_albums = "insert into albums %s values %s on duplicate key update %s;" % (
                                re.sub(r"'", "", str(tuple(temp_dict))), str(tuple(temp_dict.values())), temp_str)
                            insert_albums = re.sub(r"\n|\\|\r|\t|\r\n|\n\r", "", insert_albums)
                            self.q.put(insert_albums)
                        self.get_other_msg(other_headers, url, store_id, shop_id, page_num)
                elif json.loads(response.text)['errcode'] == 500:
                    print("请求失败" + response.url)
                    pass
                elif json.loads(response.text)['errcode'] == 9:
                    print("验证失败" + response.url)
                    pass
                else:
                    print("未知错误" + response.url)
                    pass
            else:
                print("无效地址" + response.url)

    def save_2_mysql(self):
        """
        把队列中的信息保存到数据库，对爬虫是否结实进行判断
        :return: None
        """
        end_flag = 0
        while True:
            if self.q.empty():
                if end_flag == 10:
                    break
                else:
                    end_flag += 1
                    time.sleep(3)
            else:
                end_flag = 0
                insert_albums = self.q.get()
                print(insert_albums)
                try:
                    self.crs.execute(insert_albums)
                except:
                    self.conn.ping()
                    self.crs = self.conn.cursor()
                    self.crs.execute(insert_albums)
                self.conn.commit()

    def __del__(self):
        self.crs.close()
        self.conn.close()
        print("-"*50 + "已完成爬虫" + "-"*50)

    def run(self):
        """
        主程序，用列表切割的方式手动构造多线程
        :return: None
        """
        store_list = self.select_from_store()
        cut_store_list = [store_list[i:i + self.cut_rule] for i in range(0, len(store_list), self.cut_rule)]
        t_list = list()
        for csl_mini in cut_store_list:
            t_list.append(threading.Thread(target=self.select_url, args=(csl_mini,)))
        t_list.append(threading.Thread(target=self.save_2_mysql))
        for t in t_list:
            t.start()
        for t in t_list:
            t.join()


if __name__ == '__main__':
    with open("./ip_pool", "r") as f:
        content = f.read()
    ip_pool = json.loads(content)
    bis = By_Img_Spiders(ip_pool)
    bis.run()
