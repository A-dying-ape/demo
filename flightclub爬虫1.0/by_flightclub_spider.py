# coding =utf-8
import re
import threading
import queue
import time
import pymysql
import json
import sys
import requests
from retryl_request import request_url
from urllib import parse
from lxml import etree
from deal_json_invaild import deal_json_invaild as dji


sys.setrecursionlimit(1000000)
requests.packages.urllib3.disable_warnings()


class Txt_Content_spider():

    def __init__(self, ip_pool):
        print("爬虫开启中......")
        time.sleep(1)
        self.ip_pool = ip_pool
        self.start_url = "http://www.flightclub.cn/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        self.q = queue.Queue(1000)
        self.conn = pymysql.connect(host="", port=, user="", password="",
                                    database="", charset="")
        self.crs = self.conn.cursor()

    def start_page(self):
        response = request_url(self.start_url, headers=self.headers, proxies_list=self.ip_pool)
        t_list = list()
        t1 = threading.Thread(target=self.slider_spider, args=(response,))
        t2 = threading.Thread(target=self.sale_date_spider, args=(response,))
        t3 = threading.Thread(target=self.main_page_spider, args=(response,))
        t4 = threading.Thread(target=self.get_load_api, args=(response,))
        t5 = threading.Thread(target=self.get_msg_to_mysql)
        t_list.append(t1)
        t_list.append(t2)
        t_list.append(t3)
        t_list.append(t4)
        t_list.append(t5)
        for t in t_list:
            t.start()

    def slider_spider(self, response):
        """
        获取推荐滑块的详情页url
        :param response 首页的源码
        """
        html = etree.HTML(response.text)
        sliders = html.xpath("//div[@class='swiper-wrapper']//div[@class='head_slider swiper-slide']")
        slider_list = list()
        for i in sliders:
            slider_list.append(parse.urljoin(self.start_url, str(i.xpath("./a/@href")[0])))
        self.detail_page_spider(slider_list)

    def sale_date_spider(self, response):
        """
        获取发售日历url
        :param response 首页的源码
        """
        html = etree.HTML(response.text)
        a_list = html.xpath("//div[@class='left pure-u-1']/a/@href")
        saledate_url = parse.urljoin(self.start_url, str(a_list[1]))
        saledate_text = request_url(saledate_url, headers=self.headers, proxies_list=self.ip_pool)
        saledate_html = etree.HTML(saledate_text.text)
        saledate_url_list = list()
        # 获取最新球鞋发售信息的url
        for i in saledate_html.xpath("//div[@class='release_list']/a/@href"):
            saledate_list_url = parse.urljoin(self.start_url, i)
            saledate_detail_text = request_url(saledate_list_url, headers=self.headers, proxies_list=self.ip_pool)
            saledate_detail_html = etree.HTML(saledate_detail_text.text)
            # 获取相关资讯的url(最终目的)
            for i in saledate_detail_html.xpath("//div[@class='relat_news']/a/@href"):
                saledate_url_list.append(parse.urljoin(self.start_url, i))
        self.detail_page_spider(saledate_url_list)

    def main_page_spider(self, response):
        """
        获取首页最新资讯的url
        :param response 首页的源码
        """
        global normal_item
        html = etree.HTML(response.text)
        try:
            large_item = html.xpath(
                "//div[@class='center main_news_list pure-u-1 pure-u-md-2-3']/div[@class='news_item large pure-g']/div[3]/a/@href")
            normal_item = html.xpath(
                "//div[@class='center main_news_list pure-u-1 pure-u-md-2-3']/div[@class='news_item large pure-g']/div[1]/a/@href")
        except:
            pass
        else:
            item_list = large_item + normal_item
            item_url_list = list()
            for i in item_list:
                item_url_list.append(parse.urljoin(self.start_url, i))
            self.detail_page_spider(item_url_list)

    def get_load_api(self, response):
        """
        获取加载更多的api
        :param response 首页的源码
        """
        # 获取未加载出来的api并构建url
        load_more_url = re.findall(r"var url = \"//(www\.flightclub\.cn/mapi/data/news_list_full/)\"", response.text)
        news_list_pos = 30
        path = "http://" + load_more_url[0]
        params = "?t=" + str(int(time.time() * 1000))
        self.load_more_msg(path, news_list_pos, params)

    def load_more_msg(self, path, news_list_pos, params):
        print(news_list_pos)
        load_more_url = path + str(news_list_pos) + params
        content = request_url(load_more_url, headers=self.headers, proxies_list=self.ip_pool).content.decode(
            "unicode-escape")
        try:
            # json异常预处理
            json.loads(content, strict=False)
        except:
            content = dji(content)
        finally:
            json_text = json.loads(content, strict=False)
            if json_text["msg"]["count"] == 0:
                print("已获取到所有详情页的地址！")
                return
            else:
                load_more_url_list = list()
                for i in json_text["msg"]["list"]:
                    load_more_url_list.append(parse.urljoin(self.start_url, i["url"]))
                self.detail_page_spider(load_more_url_list)
            news_list_pos = int(news_list_pos) + 30
            self.load_more_msg(path, news_list_pos, params)

    def detail_page_spider(self, url_list):
        """
        获取详情页所有信息保存到列表然后添加到队列中
        :param response 首页的源码
        <class 'str'>  title
        <class 'str'>  push_time_str
        <class 'str'>  read_count
        <class 'list'>  img_list
        <class 'str'>  text_content
        """
        for url in url_list:
            msg_dict = {"text_link": url}
            # 获取详情页信息
            response = request_url(url, headers=self.headers, proxies_list=self.ip_pool)
            html = etree.HTML(response.text)
            # 获取文字主题
            try:
                temp_title = re.sub("\\|\n", "", html.xpath("//div[@class='news_title']/h1/text()")[0])
            except:
                print(response.url)
                pass
            else:
                temp_title = re.sub("\"|'", "“", temp_title)
                msg_dict["title"] = temp_title
                # 获取文字发表时间
                msg_dict["push_time"] = html.xpath("//div[@class='body']/div[1]/text()")[0]
                # 请求阅读数api，获取阅读数量
                count_url_list = re.findall("fetch\(\"(/ajax/news_count/\d+)\"\)\.then\(function\(r\)", response.text)
                count_url = parse.urljoin(self.start_url, count_url_list[0])
                count = request_url(count_url, headers=self.headers, proxies_list=self.ip_pool)
                try:
                    msg_dict["read_count"] = count.text
                except:
                    print(url)
                    print(count_url)
                # 获取全部图片链接
                img = html.xpath("//div[@class='content']/img")
                if len(img) <= 0:
                    img = html.xpath("//div[@class='content']/p/a/img")
                img_list = list()
                for i in img:
                    temp_img = str(i.xpath("./@src")[0])
                    if temp_img.endswith(".png"):
                        try:
                            img_list.append(str(i.xpath("./@data-original")[0]))
                        except:
                            pass
                        else:
                            img_list.append(temp_img)
                    else:
                        img_list.append(temp_img)
                msg_dict["img_list"] = str(img_list)
                # 获取正文内容
                temp_re_obj = re.compile(r"<div class=\"content\">(.*?)<!-- GA -->", re.S)
                text_list = temp_re_obj.findall(response.text)
                text_content = ""
                for i in text_list:
                    text_temp = re.sub(
                        r"<(.*?)>| |&sup2;|\u200b|&yen;|&nbsp;|&ldquo;|&rdquo;|&middot;|&amp;|&mdash;|▼|\r|\n|\t|\\", "", i)
                    text_temp = re.sub("\"|'", "“", text_temp)
                    text_content += text_temp
                msg_dict["text_content"] = text_content
                self.q.put(msg_dict)

    def get_msg_to_mysql(self):
        """
        获取队列信息保存到数据库
        """
        # 指定存储的数据库，没有就创建，存在就直接用
        # create_table = """
        # create table text_spider (
        # id int(4) auto_increment primary key,
        # text_link varchar(100) unique,
        # title varchar(255),
        # push_time varchar(40),
        # read_count varchar(20),
        # img_list text,
        # text_content text
        # );
        # """
        time.sleep(1)
        # end_flag爬虫结束的标志
        end_flag = 0
        while True:
            if self.q.empty():
                if end_flag >= 10:
                    break
                end_flag += 1
                time.sleep(2)
            else:
                end_flag = 0
                msg = self.q.get()
                temp_str = ""
                for i in tuple('%s = "%s",' % (k, v) for k, v in msg.items()):
                    temp_str += i
                temp_str = temp_str[0:-2] + "\""
                insert_msg = "insert into text_spider %s values %s on duplicate key update %s;" % (
                re.sub("'", "", str(tuple(msg))), str(tuple(msg.values())), temp_str)
                try:
                    self.crs.execute(insert_msg)
                except:
                    self.conn.ping()
                    self.crs = self.conn.cursor()
                    try:
                        self.crs.execute(insert_msg)
                    except:
                        print(insert_msg)
                self.conn.commit()

    def __del__(self):
        # 关闭数据库连接
        self.crs.close()
        self.conn.close()
        print("-" * 50 + "已完成全站爬虫" + "-" * 50)

    def run(self):
        self.start_page()


if __name__ == '__main__':
    with open("./ip_pool", "r") as f:
        content = f.read()
    ip_pool = json.loads(content)
    TCS = Txt_Content_spider(ip_pool)
    TCS.run()
