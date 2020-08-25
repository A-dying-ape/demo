# -*- coding: utf-8 -*-
# coding:gbk
import re
import time
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from urllib import parse
from tbspider.items import TbspiderGoodsItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com', 'detail.tmall.com', 'rate.tmall.com']
    start_urls = ['http://taobao.com/']
    store = input("请输入商店名称：")
    driver = webdriver.Chrome("C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver.exe")
    wait = WebDriverWait(driver, 10)

    def start_requests(self):
        total, self.cookies = self.get_total_page()
        # print(self.cookies)
        total = int(re.compile(r"(\d+)").search(total).group(1))
        for i in range(1, total + 1):
            time.sleep(2)
            input = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
            submit = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(i)
            submit.click()
            self.wait.until(EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(i)))
            goods_item = TbspiderGoodsItem()
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
            html = self.driver.page_source
            # for i in range(0, 45):
            #     with open("./tb" + str(i), "w", encoding="utf-8") as f:
            #         f.write(html)
            doc = pq(html)
            items = doc('#mainsrp-itemlist .items .item').items()
            for item in items:
                goods_item['img'] = parse.urljoin(self.start_urls[0], item.find('.J_ItemPic').attr('data-src')),
                goods_item['price'] = item.find('.price').text(),
                goods_item['pay_num'] = item.find('.deal-cnt').text()[:-3],
                goods_item['title'] = item.find('.title').text(),
                goods_item['shop'] = item.find('.shop').text(),
                goods_item['location'] = item.find('.location').text(),
                goods_item['href'] = parse.urljoin(self.start_urls[0], item.find('.J_ClickStat').attr('href'))
                # print(type(parse.urljoin(self.start_urls[0], item.find('.J_ClickStat').attr('href'))))
                yield scrapy.FormRequest(
                    goods_item['href'],
                    formdata=self.cookies,
                    callback=self.parse,
                    meta={"item": goods_item}
                )

    def get_total_page(self):
        self.driver.get(self.start_urls[0])
        input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(self.store)
        submit.click()
        total = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        cookies = {i['name']: i['value'] for i in self.driver.get_cookies()}
        return total.text, cookies

    def parse(self, response):
        # print(response.url)
        # with open("tb.html","w",encoding="utf-8") as f:
        #     try:
        #         f.write(response.body.decode('utf-8'))
        #     except:
        #         f.write(response.body.decode('gbk'))
        global detail_msg, data, temId, sellerId
        goods_item = response.meta['item']
        try:
            data = response.body.decode("utf-8")
        except:
            data = response.body.decode("gbk")
        finally:
            try:
                detail_msg = re.search(r"\"groupProps\":\s?(\[.*\]),\"propsList\"", data).group(1)
            except:
                detail_msg = None
            finally:
                goods_item['detail_dict'] = detail_msg
                try:
                    temId = re.search(r"\"itemId\":\s?(\d+),", data).group(1)
                except:
                    try:
                        temId = re.search(r"itemId=(\d+)", data).group(1)
                    except:
                        # print(response.url+"*"*50)
                        temId = None
                try:
                    sellerId = re.search(r"sellerId=(\d+)", data).group(1)
                except:
                    try:
                        sellerId = re.search(r"sellerId:\s?(\d+)", data).group(1)
                    except:
                        # print(response.url + "*" * 50)
                        sellerId = None
        comment_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId={}".format(temId, sellerId)
        yield scrapy.FormRequest(
            comment_url,
            formdata=self.cookies,
            callback=self.get_comment,
            meta={"item": goods_item}
        )

    def get_comment(self, response):
        global data
        # print(response.url)
        with open("comment.html","w",encoding="utf-8") as f:
            try:
                f.write(response.body.decode('utf-8'))
            except:
                f.write(response.body.decode('gbk'))
        good_item = response.meta['item']
        try:
            data = response.body.decode("utf-8")
        except:
            data = response.body.decode("gbk")
        finally:
            comment_msg = re.findall(r"\"rateContent\":\s?:\"(.*)\"", data)
        good_item['comment'] = comment_msg if len(comment_msg) > 0 else None
        print(response.url)
        yield good_item
