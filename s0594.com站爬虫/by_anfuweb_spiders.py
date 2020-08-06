import requests
import re
import retryl_parse
from by_img_spiders import By_Img_Spiders
from lxml import etree
from urllib import parse


class By_Anfuweb_Spiders():

    def __init__(self):
        self.start_url = "http://www.s0594.com/"
        self.index_headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
        self.tr_len = 12
        self.url_list = list()

    def nav_url_spider(self):
        response = requests.get(self.start_url, headers=self.index_headers)
        nav_html = etree.HTML(response.text)
        nav_hrefs = nav_html.xpath("//div[@class='htmlMenu']/ul/li/a/@href")
        nav_href_list = [parse.urljoin(self.start_url,href) for href in nav_hrefs]
        return nav_href_list

    def store_url_spider(self, url, store_href_list, flag=-1):
        global next_href_list
        response = requests.get(url, headers=self.index_headers)
        html = etree.HTML(response.text)
        store_html = html.xpath("//div[@class='shops']/ul/li/div[@class='shopname']/a[last()]/@href")
        for store_href in store_html:
            store_href_list.append(parse.urljoin(self.start_url, str(store_href)))
        try:
            page_num = str(html.xpath("//div[@class='sdwl_search_main_page_bottom1'][1]/a[@class='now_page']/text()")[0])
        except:
            print("导航栏推荐商家" + url)
        else:
            if page_num == '1':
                next_page_href = html.xpath("//div[@class='sdwl_search_main_page_bottom1'][1]/a/@href")
                next_href_list = list()
                for next_href in list(set(next_page_href)):
                    next_href_list.append(parse.urljoin(self.start_url, next_href))
            if flag >= len(next_href_list) - 1:
                self.get_store_msg(store_href_list)
                return
            flag += 1
            self.store_url_spider(next_href_list[flag], store_href_list, flag)

    def get_store_msg(self, store_href_list):
        global smsg_html
        for store_href in store_href_list:
            if "#" or "?" in store_href:  # 请求的地址中存在标签#或者参数？，阻止了请求正确的页面
                store_href = re.sub(r'[#?]', "", store_href)
            response = retryl_parse.parse_url(url=store_href, headers=self.index_headers)
            try:
                smsg_html = etree.HTML(response.text)
            except:
                print(store_href)
            tr_list = smsg_html.xpath("//table/tbody/tr")
            store_dict = dict()
            for num in range(self.tr_len):
                if num == 0:
                    # 这里留着数据扩充抓取
                    pass
                elif num == 1:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 2:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/a/@href")[0]).strip()
                        if len(store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]]) != 0:
                            self.url_list.append(str(tr_list[num].xpath("./td[2]/a/@href")[0]).strip())
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 3:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/a/@href")[0]).strip()
                        if len(store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]]) != 0:
                            self.url_list.append(str(tr_list[num].xpath("./td[2]/a/@href")[0]).strip())
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 4:
                    # 这里留着数据扩充抓取
                    pass
                elif num == 5:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                        store_dict["QQ1在线联系接口"] = str(tr_list[num].xpath("./td[2]/a/@href")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 6:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                        store_dict["QQ2在线联系接口"] = str(tr_list[num].xpath("./td[2]/a/@href")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 7:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 8:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 9:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = str(
                            tr_list[num].xpath("./td[2]/text()")[0]).strip()
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/div/text()")[0]] = ""
                elif num == 10:
                    try:
                        store_dict[tr_list[num].xpath("./td[1]/text()")[0]] = parse.urljoin(self.start_url, str(
                            tr_list[num].xpath("./td[2]/img/@src")[0]).strip())
                    except:
                        store_dict[tr_list[num].xpath("./td[1]/text()")[0]] = ""
                elif num == 11:
                    try:
                        store_dict[tr_list[num - 2].xpath("./following-sibling::td[1]/div/text()")[0]] = \
                        tr_list[num - 2].xpath("./following-sibling::td[2]/text()")[0].strip()
                    except:
                        store_dict[tr_list[num - 2].xpath("./following-sibling::td[1]/div/text()")[0]] = ""
            print(store_dict)


    def run(self):
        nav_href_list = self.nav_url_spider()
        for nav_href in nav_href_list:
            self.store_url_spider(nav_href, list())
        By_Img_Spiders(self.url_list).run()


if __name__ == '__main__':
    bas = By_Anfuweb_Spiders()
    bas.run()