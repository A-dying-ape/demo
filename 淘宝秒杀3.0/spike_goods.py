import requests
import parsel
import re
import json
import random
import time
import queue
from threading import Thread
from urllib import parse


q_c = queue.Queue()
q = queue.Queue()


def get_detail_params(url, page_source, c):
    selector = parsel.Selector(page_source)
    seller_id = selector.xpath("//form[@id='J_FrmBid']/input[@name='seller_id']/@value").get()
    photo_url = selector.xpath("//form[@id='J_FrmBid']/input[@name='photo_url']/@value").get()
    rootCatId = selector.xpath("//form[@id='J_FrmBid']/input[@name='rootCatId']/@value").get()
    allow_quantity = re.findall("\"quantity\":(\d+),", page_source)[0]
    param = re.findall("id=(\d+).*&skuId=(\d+)", url)[0]
    buy_param = param[0] + "_" + "1" + "_" + param[1]
    _tb_token_ = c.get("_tb_token_")
    skuId = param[1]
    item_id_num = param[0]
    item_id = param[0]
    auction_id = param[0]
    buy_now = re.findall("\"price\":\"(\d+\.\d+)\",", page_source)[0]
    current_price = buy_now
    seller_num_id = selector.xpath("//*[@id=\"dsr-userid\"]/@value").get()
    data = {
        'title': '(unable to decode value)',
        'x_id': '',
        'seller_id': seller_id,
        'seller_nickname': '(unable to decode value)',
        'who_pay_ship': '(unable to decode value)',
        'photo_url': photo_url,
        'region': '(unable to decode value)',
        'auto_post': 'false',
        'etm': 'post',
        'virtual': 'false',
        'rootCatId': rootCatId,
        'auto_post1': '',
        'buyer_from': 'ecity',
        'root_refer': '',
        'item_url_refer': 'https%3A%2F%2Fs.taobao.com%2F',
        'allow_quantity': allow_quantity,
        'buy_param': buy_param,
        'quantity': '1',
        '_tb_token_': _tb_token_,
        'skuInfo': '(unable to decode value)',
        'use_cod': 'false',
        '_input_charset': 'UTF-8',
        'destination': '350100',
        'skuId': skuId,
        'bankfrom': '',
        'from_etao': '',
        'item_id_num': item_id_num,
        'item_id': item_id,
        'auction_id': auction_id,
        'seller_rank': '0',
        'seller_rate_sum': '0',
        'is_orginal': 'no',
        'point_price': 'false',
        'secure_pay': 'true',
        'pay_method': '(unable to decode value)',
        'from': 'item_detail',
        'buy_now': buy_now,
        'current_price': current_price,
        'auction_type': 'b',
        'seller_num_id': seller_num_id,
        'activity': '',
        'chargeTypeId': '',
    }
    return data, param[0]


def confirm_order(g_data, ref_url, session, c, ip_pool, proxy_flag, updata_log):
    url = "https://buy.tmall.com/order/confirm_order.htm"
    headers = {
        "Origin": "https://detail.tmall.com",
        "Referer": ref_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    }
    params = {
        "x-itemid": g_data.get("item_id_num"),
        "x-uid": c.get("unb")
    }
    start_time = time.time()
    if proxy_flag:
        session.proxies.update(random.choice(ip_pool))
    response = session.post(url, headers=headers, data=g_data, params=params)
    try:
        res = re.search(r"var orderData= \{.*\{\"data\":\[\]\},\"reload\":true\}",response.text).group()
        res = re.findall("var orderData= (.*)", res)
        res = json.loads(json.loads(json.dumps(res), encoding="utf-8")[0])
    except:
        res = re.findall(r"亲，小二正忙", response.text)
        if len(res) > 0:
            updata_log.emit("抢购失败，可能商品已经买完，也可能网络请求慢了！")
            return None, None, None, None, None
    else:
        print(res)
        secretvalue = res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("secretValue")
        sparam1 = res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("sparam1")

        endpoint = parse.quote(json.dumps(res.get("endpoint")).replace(": ", ":").replace(", ", ","))

        linkage = {}
        linkage["common"] = res.get("linkage").get("common")
        linkage["signature"] = res.get("linkage").get("signature")
        linkage = parse.quote(json.dumps(linkage).replace(": ", ":").replace(", ", ","))

        p_data = {}
        for k, v in res.get("data").items():
            if res.get("data").get(k).get("submit"):
                p_data[k] = res.get("data").get(k)
        p_data = parse.quote(json.dumps(p_data).replace(": ", ":").replace(", ", ","))

        action = res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("action")

        _tb_token_ = g_data.get("_tb_token_")

        event_submit_do_confirm = res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("event_submit_do_confirm")

        praper_alipay_cashier_domain = "cashierrz" + res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("unitSuffix")[2:]

        input_charset = res.get("data").get("submitOrderPC_1").get("hidden").get("extensionMap").get("input_charset")

        hierarchy = parse.quote(json.dumps(res.get("hierarchy").get("structure")).replace(": ", ":").replace(", ", ","))

        data = {
            "endpoint": endpoint,
            "linkage": linkage,
            "data": p_data,
            "action": action,
            "_tb_token_": _tb_token_,
            "event_submit_do_confirm": event_submit_do_confirm,
            "praper_alipay_cashier_domain": praper_alipay_cashier_domain,
            "input_charset": input_charset,
            "hierarchy": hierarchy,
        }
        return data, secretvalue, sparam1, response.url, start_time


def submit_order(c_data, itemid, secretvalue, sparam1, c_url, session, c, ip_pool, updata_log, u_name, proxy_flag):
    url = "https://buy.tmall.com/auction/confirm_order.htm"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        'Referer': c_url,
        'Origin': "https://buy.tmall.com",
    }
    params = {
        'x-itemid': itemid,
        'x-uid': c.get("unb"),
        'submitref': secretvalue,
        'sparam1': sparam1
    }
    if proxy_flag:
        session.proxies.update(random.choice(ip_pool))
    response = session.post(url, headers=headers, params=params, data=c_data)
    print(response.text)
    end_time = time.time()
    flag = re.findall("<p class=\"youxianchupin\">正在创建支付宝安全链接...</p>", response.text)
    if len(flag) > 0:
        q_c.put(u_name)
        updata_log.emit("%s秒杀成功！" % u_name)
    else:
        updata_log.emit("%s秒杀失败！" % u_name)
    return end_time


def main(url, q, ip_pool, page_source, updata_log, proxy_flag):
    # print(time.time())
    session = requests.session()
    c = q.get()
    u_name = parse.unquote(c.get("lgc")).encode("utf-8").decode('unicode_escape')
    for k, v in c.items():
        session.cookies.set(k, v)
    g_data, itemid = get_detail_params(url, page_source, c)
    c_data, secretvalue, sparam1, c_url, start_time = confirm_order(g_data, url, session, c, ip_pool, proxy_flag, updata_log)
    if (c_data is not None) and (secretvalue is not None) and (sparam1 is not None) and (c_url is not None) and (start_time is not None):
        end_time = submit_order(c_data, itemid, secretvalue, sparam1, c_url, session, c, ip_pool, updata_log, u_name, proxy_flag)
        updata_log.emit("用时:%s秒" % (end_time - start_time))
    else:
        updata_log.emit("%s秒杀失败！" % u_name)


def run(url, ip_pool, cookie_list, page_source, updata_log, proxy_flag, spike_count):
    t_list = []
    for cookie in cookie_list:
        q.put(cookie)
    for i in range(q.qsize()):
        t_list.append(Thread(target=main, args=(url, q, ip_pool, page_source, updata_log, proxy_flag)))
    for t in t_list:
        t.start()
        t.join()
    spike_count.emit(str(q_c.qsize()))