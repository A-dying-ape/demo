# coding:utf-8
import requests
import json
import random


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}
url_list = ["http://http.tiqu.alicdns.com/getip3?num=400&type=2&pro=350000&city=350500&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=", "http://webapi.http.zhimacangku.com/getip?num=400&type=2&pro=350000&city=350500&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions="]
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
with open("./ip_pool", "a") as f:
    f.write(json.dumps(ip_pool))