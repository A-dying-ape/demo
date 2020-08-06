# coding:utf-8
"""
获取代理IP接口，请求IP构造IP池，IP池是一个json字符串
name是一个http://+abcdefghijklmnopqrstuvwxyz01234546789ABCDEFGHIJKLMNOPQRSTUVWXYZ中随机的挑选的8位字符串
value是对应代理IP接口返回的IP
写入并保存到ip_pool文件下
"""
import requests
import json
import random


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}
url_list = ["http://http.tiqu.alicdns.com/getip3?num=400&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=5&mr=1&regions=&gm=4","http://http.tiqu.alicdns.com/getip3?num=400&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=5&mr=1&regions=","http://webapi.http.zhimacangku.com/getip?num=400&type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=5&mr=1&regions="]
name_str = "abcdefghijklmnopqrstuvwxyz01234546789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ip_pool = list()
for url in url_list:
    response = requests.get(url, headers=headers)
    json_info = json.loads(response.text)
    for ip in json_info['data']:
        code_id = ""
        for i in random.sample(name_str, 8):
            code_id += i
        ip_pool.append({code_id:"http://" + ip['ip'] + ":" + str(ip['port'])})
with open("./ip_pool", "w") as f:
    f.write(json.dumps(ip_pool))