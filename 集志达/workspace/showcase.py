from util.request import request_url
from setting import HEADERS, NAV_MENU
from lxml import etree
from urllib import parse
import time
import os


class Show_Case():
    def __init__(self, state_url, it):
        self.state_url = state_url
        self.it = it

    def get_menu_href(self):
        # 获取分类菜单的url
        response = request_url(url=self.it, headers=HEADERS, method="get", proxy=True)
        html = etree.HTML(response.text)
        nav_text = html.xpath("//ul[@class='temp_dl_dt_ul']/a//text()")
        for text in nav_text:
            if text.strip() in list(set(NAV_MENU)):
                temp_dict = {}
                nav_href = html.xpath("//ul[@class='temp_dl_dt_ul']/a/li[text()='%s']/../@href" %text.strip())[0].strip()
                nav_href = parse.urljoin(self.it, nav_href)
                temp_dict["url"] = nav_href
                temp_dict["text"] = text
                yield temp_dict

    def get_detail(self, url, kid):
        path = "./case_img/%s" % kid
        try:
            os.mkdir(path)
        except:
            pass
        response = request_url(url=url, headers=HEADERS, method='get', proxy=True)
        time.sleep(1)
        html = etree.HTML(response.text)
        cur_page = html.xpath("//div[@class='pager']/span/label[@name='curpage']/text()")[0].strip()
        tot_page = html.xpath("//div[@class='pager']/span/label[@name='totalpage']/text()")[0].strip()
        # 获取一个类别下的所有数据
        div_list = html.xpath("//ul[@class='anli_ul']/li/div")
        for div in div_list:
            text = div.xpath("./div[2]/text()")[0].strip()
            code_img = div.xpath("./div[1]/div/div/div/img/@src")[0].strip()
            code_img = parse.urljoin(self.state_url, code_img)
            img = request_url(url=code_img, headers=HEADERS, method='get', proxy=True)
            if img.content:
                time.sleep(0.5)
                # 保存数据
                with open(path + "/" + text + ".png", 'wb') as f:
                    f.write(img.content)
        # 翻页
        next_page = html.xpath("//div[@class='pager']/a[@class='frame-btn page-next']/@href")[0].strip()
        next_page = parse.urljoin(url, next_page)
        if cur_page >= tot_page:
            return
        else:
            self.get_detail(next_page, kid)

    def run(self):
        nav_dict = self.get_menu_href()
        for nh in nav_dict:
            url = nh.get("url")
            kid = nh.get("text")
            self.get_detail(url, kid)