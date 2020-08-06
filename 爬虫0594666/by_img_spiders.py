# coding:utf-8
import requests
import re
import time
import random
import json
import sys
import get_cookies
import pymysql
from lxml import etree
from urllib import parse
from retryl_request import request_url
from url_parse import parse_url


sys.setrecursionlimit(1000000)


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

    def select_from_store(self):
        try:
            self.crs.execute("select * from store where ID > 1265")
        except:
            self.conn.ping()
            self.crs = self.conn.cursor()
            self.crs.execute("select * from store where ID > 1265")
        final_temp_list = list()
        for store in self.crs.fetchall():
            temp_list = list()
            temp_list.append(store[0])
            if store[5] is not None:
                temp_list.append(store[5])
            elif store[6] is not None:
                temp_list.append(store[6])
            final_temp_list.append(temp_list)
        return final_temp_list

    def select_url(self, store_list):
        for msg_list in store_list:
            for url in msg_list[1:len(msg_list)]:
                if "yupoo.com" in url:
                    if url.startswith("http://") or url.startswith("https://"):
                        self.yupoo_url_handl(url, msg_list[0])
                    elif not url.split(":")[1].startswith("//"):
                        url = url.split(":")[0] + "://" + url.split(":")[1]
                        self.yupoo_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.yupoo_url_handl(url, msg_list[0])
                elif "w.url.cn" in url:
                    if url.startswith("http"):
                        self.yupoo_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                elif "suo.im" in url:
                    if url.startswith("http"):
                        self.yupoo_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                elif "szwego.com" in url:
                    if url.startswith("http"):
                        self.yupoo_url_handl(url, msg_list[0])
                    else:
                        url = "http://" + url
                        self.other_url_handl(url, msg_list[0])
                else:
                    pass
                    # self.err_url_handl(url, msg_list[0])

    def yupoo_url_handl(self, old_url, store_id):
        response = request_url(old_url, headers=self.headers, proxies_list=self.ip_pool)
        if response.status_code is not None:
            html = etree.HTML(response.text)
            try:
                albums_url = html.xpath("//div[@class='showheader__menus']/a[2]/@href")[0]
            except:
                print("用户账号被冻结:" + old_url)
            else:
                new_url = parse.urljoin(response.url, albums_url)
                self.yupoo_spider(new_url, store_id)
        else:
            print("错误页面" + old_url)

    def other_url_handl(self, url, store_id):
        other_headers = None
        response = request_url(url, headers=self.headers, proxies_list=self.ip_pool)
        try:
            shop_id = re.search(r"/shop_detail/(\w\d+)", response.url).group(1)
        except:
            print(response.url)
        else:
            if response is not None:
                cookies, base_url = get_cookies.get_cookies(url, ip_pool)
                url = parse_url(base_url.lower(), self.server_url, "")
                for item in cookies:
                    other_headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                        "cookie": "%s=%s" % (item.name, item.value)
                    }
                self.get_other_msg(other_headers, url, store_id, shop_id)

    def err_url_handl(self, url, store_dict):
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
        response = request_url(yupoo_url, headers=self.headers, proxies_list=self.ip_pool)
        try:
            html = etree.HTML(response.text)
        except:
            print("请求失败：" + yupoo_url)
            pass
        else:
            if len(re.findall(r"该用户主页暂时关闭", response.text)) > 0:
                print("该用户主页暂时关闭:" + yupoo_url)
            elif html.xpath("//a[@class='showheader__menuslink showheader__active']/text()")[0] == "相册":
                temp_albums_list = html.xpath("//div[@class='showindex__parent']/div/a/@href")
                for albums in temp_albums_list:
                    self.get_ypimg_page(parse.urljoin(response.url, albums), store_id)
                if len(html.xpath("//div[@class='none_select pagination__buttons']/a[@title='后一页']/@href")) == 0:
                    print("一个网址爬取完毕！")
                else:
                    next_page = html.xpath("//div[@class='none_select pagination__buttons']/a[@title='后一页']/@href")[0]
                    next_page = parse.urljoin(response.url, next_page)
                    self.yupoo_spider(next_page, store_id)
            else:
                print("未知错误：" + yupoo_url)

    def get_ypimg_page(self, albums_href, store_id):
        response = request_url(albums_href, headers=self.headers, proxies_list=self.ip_pool)
        try:
            html = etree.HTML(response.text)
        except:
            print("请求失败：" + albums_href)
            pass
        else:
            albums_name = html.xpath("//div[@class='showalbumheader__gallerydec']/h2/span[1]/text()")[0]
            albums_name = re.sub("\"|'", "“", albums_name)
            # albums_count = html.xpath("//div[@class='showalbumheader__gallerydec']/h2/span[2]/text()")
            # pic_src = html.xpath("//div[@class='showalbum__parent showalbum__nor nor']//img/@src")
            other_msg = html.xpath("//div[@class='showalbumheader__gallerydec']/div[1]/text()")
            other_msg = re.sub("\"|'", "“", str(other_msg))
            data_id = html.xpath(
                "//div[@class='showalbum__parent showalbum__nor nor']/div[@class='showalbum__children image__main']/@data-id")
            img_href = list()
            for id in data_id:
                img_url = parse_url(albums_href, id, "uid=1")  # &tab=min 请求缩略版图片
                img_href.append(img_url)
            img_href = str(img_href)
            albums_info = (albums_name, store_id, albums_href, img_href, str(other_msg))
            insert_albums = "insert into albums (albums_name,store_id,albums_href,img_url,other_msg) values %s on duplicate key update %s;" % (
            str(albums_info),
            """albums_name="%s",store_id=%s,albums_href="%s",img_url="%s",other_msg="%s" """ % albums_info)
            insert_albums = re.sub(r"\\|\n", "", insert_albums)
            print(insert_albums)
            try:
                self.crs.execute(insert_albums)
            except:
                self.conn.ping()
                self.crs = self.conn.cursor()
                self.crs.execute(insert_albums)
            self.conn.commit()

    def get_other_msg(self, other_headers, url, store_id, shop_id, page_num=1):
        params = {
            "page_index": page_num,
            "act": "single_album",
            "shop_id": shop_id,
            "time_stamp": int(time.time() * 1000),
        }
        response = requests.get(url, params=params, proxies=random.choices(self.ip_pool)[0], headers=other_headers)
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
                    # temp_dict["albums_name"] = re.sub(r"\n|\\", "", temp_dict["albums_name"])
                    temp_dict["store_id"] = store_id
                    temp_dict["albums_href"] = img["link"]
                    temp_dict["other_msg"] = str("店铺:" + re.sub("\"|'", "“", img["shop_name"]) + ",上架时间：" + img["old_time"])
                    temp_str = ""
                    for i in tuple('%s = "%s",' % (k, v) for k, v in temp_dict.items()):
                        temp_str += i
                    temp_str = temp_str[0:-2] + "\""
                    insert_albums = "insert into albums %s values %s on duplicate key update %s;" % (
                        re.sub(r"'", "", str(tuple(temp_dict))), str(tuple(temp_dict.values())), temp_str)
                    insert_albums = re.sub(r"\\|\n", "", insert_albums)
                    print(insert_albums)
                    try:
                        self.crs.execute(insert_albums)
                    except:
                        self.conn.ping()
                        self.crs = self.conn.cursor()
                        self.crs.execute(insert_albums)
                    self.conn.commit()
                self.get_other_msg(other_headers, url, store_id, shop_id, page_num)
        elif json.loads(response.text)['errcode'] == 500:
            print(response.url)
            print("请求失败")
            pass
        elif json.loads(response.text)['errcode'] == 9:
            print("验证失败")
            pass
        else:
            print("未知错误")
            pass

    def __del__(self):
        print("-"*50 + "爬虫完成" + "-"*50)
        self.crs.close()
        self.conn.close()

    def run(self):
        store_list = self.select_from_store()
        self.select_url(store_list)


if __name__ == '__main__':
    with open("./ip_pool", "r") as f:
        content = f.read()
    ip_pool = json.loads(content)
    bis = By_Img_Spiders(ip_pool)
    bis.run()
