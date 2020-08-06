"""
https://help.aliyun.com/document_detail/32026.html?spm=a2c4g.11186623.2.22.b4c25fff20gPe2
"""
import re
import time
import warnings
from multiprocessing import Process, Queue
from bucket.bucket_setting import ip_pool
from mysql_pool.sql_pool import ConnMysql
from bucket.by_bucket import Bucket_Obj_Upload
from tool_package.retryl_request import request_url


warnings.filterwarnings('ignore')


class Upload_Img():
    def __init__(self):
        self.q = Queue(10000)
        self.limit_cont = 1
        self.limit_start = 0

    def get_img_2_mysql(self):
        conn = ConnMysql()
        while True:
            sql = "select id,store_id,albums_href,img_url from albums order by id limit {0},{1};".format(self.limit_start, self.limit_cont)
            result = conn.sql_select_one(sql)
            if len(result) < 1:
                print("-"*50 + "数据库读取完毕" + "-"*50)
                break
            self.q.put(result)
            self.limit_start += 1

    def upload_object(self):
        end_count = 0
        while True:
            if end_count > 10:
                break
            if self.q.empty():
                time.sleep(10)
                end_count += 1
            else:
                end_count = 0
                info = self.q.get()
                with open("text", "a") as f:
                    f.write(str(info["id"]) + ", ")
                img_url_list = re.sub(r"\[|\]|\'", "", info['img_url']).split(",")
                if "yupoo" in info['albums_href']:
                    headers = {
                        "Referer": info['albums_href'],
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
                    }
                    if len(img_url_list) > 0:
                        for img_url in img_url_list:
                            response = request_url(img_url, headers=headers, proxies_list=ip_pool, verify=False)
                            if response is None:
                                print(info)
                                print(img_url)
                                continue
                            img_name = "yupoo/" + str(info['store_id']) + "/" + str(info['id']) + "/" + str(
                                int(time.time() * 1000)) + ".jpg"
                            Bucket_Obj_Upload().put_object(img_name, response)
                elif "szwego" in info['albums_href']:
                    headers = {
                        "Referer": info['albums_href'],
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
                    }
                    if len(img_url_list) > 0:
                        for img_url in img_url_list:
                            response = request_url(img_url, headers=headers, proxies_list=ip_pool, verify=False)
                            if response is None:
                                print(info)
                                print(img_url)
                                continue
                            img_name = "szwego/" + str(info['store_id']) + "/" + str(info['id']) + "/" + str(
                                int(time.time() * 1000)) + ".jpg"
                            Bucket_Obj_Upload().put_object(img_name, response)
                else:
                    print(info)

    def run(self):
        process_list = []
        process_list.append(Process(target=self.get_img_2_mysql))
        for p in range(10):
            process_list.append(Process(target=self.upload_object))
        for process in process_list:
            process.start()
        for process in process_list:
            process.join()
        print("-"*50 + "全部数据上传完毕" + "-"*50)


if __name__ == '__main__':
    ui = Upload_Img()
    ui.run()
