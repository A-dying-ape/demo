import requests
import parsel
import time
from fake_useragent import UserAgent


url = "https://blog.csdn.net/xiaoxin_OK?spm=1000.2115.3001.5343"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"}
response = requests.get(url, headers=headers)
selector = parsel.Selector(response.text)
res = selector.xpath('//div[@class="article-list"]/div/h4/a/@href').getall()
for i in res:
    time.sleep(30)
    headers = {'User-Agent': str(UserAgent().random)}
    requests.get(i, headers=headers)
