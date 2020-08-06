from retryl_request import request_url
from get_cookies import get_cookies
from url_parse import parse_url
import json
import time
import re
import random
import requests


url_list = ["https://a202006181424274600171644.szwego.com/static/index.html#/shop_detail/A20200618142427460017164",
"https://A201809221834584460013518.szwego.com/static/index.html#/shop_detail/A20180922183458446001351",
"https://A201809220201599970142851.szwego.com/static/index.html#/shop_detail/A20180922020159997014285",
"https://a201902181834324600159137.szwego.com/static/index.html#/shop_detail/A20190218183432460015913",
"https://A2018012117513522656.szwego.com/static/index.html#/shop_detail/A2018012117513522656",
"https://www.szwego.com/static/index.html#/shop_detail/A201805230327120440077871",
"https://A2018020512594441423.szwego.com/static/index.html#/shop_detail/A2018020512594441423",
"https://A201902051714405060103636.szwego.com/static/index.html#/shop_detail/A20190205171440506010363",
"https://www.szwego.com/static/index.html?t=1589450027840#/shop_detail/A2018031709453701529",
"https://A2018012117513522656.szwego.com/static/index.html#/shop_detail/A2018012117513522656",
"https://www.szwego.com/static/index.html?t=1589782117420#/shop_detail/A2017122618525218256",
"https://A201904121722028100158593.szwego.com/static/index.html#/shop_detail/A20190412172202810015859",
"https://A2017101700254901629.szwego.com/static/index.html#/shop_detail/A2017101700254901629",
"https://A201809021518264490032129.szwego.com/static/index.html#/shop_detail/A20180902151826449003212",
"https://A201811012103273550124065.szwego.com/static/index.html#/shop_detail/A20181101210327355012406",
"https://A2018011513051223102.szwego.com/static/index.html#/shop_detail/A2018011513051223102"]
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
        }
with open("./ip_pool", "r") as f:
    content = f.read()
ip_pool = json.loads(content)
server_url = "service/album/get_album_themes_list.jsp"
for url in url_list:
    response = requests.get(url, proxies=random.choices(ip_pool)[0], headers=headers)
    shop_id = re.search(r"/shop_detail/(.*)", response.url).group(1)
    if response is not None:
        cookies, base_url = get_cookies(url, ip_pool)
        url = parse_url(base_url.lower(), server_url, "")
        for item in cookies:
            other_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
                # "cookie": "%s=%s" % (item.name, item.value)
                "cookie": "UM_distinctid=172fef76482421-09a957e7ea6b66-4353761-144000-172fef764838c7; "
                          "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22A202007011648174290197177%22%2C%22first_id%22%3A%22172fef75cf638b-0c1df4c5ab5928-4353761-1327104-172fef75cf78d9%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22172fef75cf638b-0c1df4c5ab5928-4353761-1327104-172fef75cf78d9%22%7D; "
                          "token=Mzk4MDk3Q0E5RTZCN0I1MkYwMTYwNDlCQUNFNkQ5QzVFOEZCOTI1OEEwOTA2MDc0QzUzRTVCNDVDMTg1RTgzRTZBNTY1MTZDQTNFNDFCRkI2ODZGRTgxRjQxRDU3MEZD; "
                          "CNZZDATA1275056938=120497081-1594357916-%7C1594363316; "
                          "JSESSIONID=B74EC8A017C3DDD861F3E6E17F3D6C3A"
                }
        params = {
            "page_index": 1,
            "act": "single_album",
            "shop_id": shop_id,
            "time_stamp": int(time.time() * 1000),
        }
        response = requests.get(url, params=params, proxies=random.choices(ip_pool)[0], headers=other_headers)
        try:
            print(url)
            img_dict = json.loads(response.text)['result']['goods_list']
        except:
            pass
            # print(url)
        else:
            if len(img_dict) <= 0:
                print("完成")
                print(url+"*")
            else:
                for img in img_dict:
                    temp_dict = dict()
                    temp_dict["img_url"] = img['imgs']
                    temp_dict["albums_name"] = img['title']
                    temp_dict["store_id"] = 1
                    temp_dict["albums_href"] = url
                    temp_dict["other_msg"] = str("店铺:" + img["shop_name"] + ",上架时间：" + img["old_time"] + ",相册连接：" + img["link"])
                    temp_str = ""
                    for i in tuple(" %s = '%s', " % (k, v) for k, v in temp_dict.items()):
                        temp_str += i
                    insert_albums = "insert into albums %s values %s on duplicate key update %s;" % (
                        re.sub(r"'", "", str(tuple(temp_dict))), str(tuple(temp_dict.values())), temp_str[0:-2])
                    # print(insert_albums)

