"""
https://help.aliyun.com/document_detail/32026.html?spm=a2c4g.11186623.2.22.b4c25fff20gPe2
update: 2020/8/1 9:58:08
author: 一只快死的猿
"""
import re
import time
import warnings
from multiprocessing import Process, Queue
from bucket.bsetting import ip_pool
from sqlpool.pool import ConnMysql
from bucket.bybucket import Bucket_Obj_Upload
from toolpackage.retry import request
from toolpackage.hash import md5hash, sha1hash


warnings.filterwarnings('ignore')


class Upload_Img():
    def __init__(self):
        self.q = Queue()
        self.limit_cont = 10000000
        self.limit_start = 0

    def get_img_2_mysql(self):
        conn = ConnMysql()
        sql = "select * from albums order by id limit {0},{1};".format(self.limit_start, self.limit_cont)
        result = conn.sql_select_many(sql)
        for i in result:
            self.q.put(i)

    def upload_object(self):
        end_count = 0
        bou = Bucket_Obj_Upload()
        while True:
            if end_count > 10:
                break
            if self.q.empty():
                time.sleep(10)
                end_count += 1
            else:
                end_count = 0
                info = self.q.get()
                img_url_list = re.sub(r"\[|\]|\'", "", info["img_url"]).split(",")
                headers = {
                    "Referer": info["albums_href"],
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
                }
                if len(img_url_list) > 0:
                    temp_list = []
                    for img_url in img_url_list:
                        response = request(img_url, headers=headers, proxies_list=ip_pool, verify=False)
                        if response is None:
                            print(info)
                            print("response is None:" + img_url)
                            continue
                        fsize = response.headers.get("Content-Length")
                        if fsize is None:
                            print(info)
                            print("fsize is None" + img_url)
                            continue
                        fmd5 = md5hash(response.content)
                        fsha1 = sha1hash(response.content)
                        code_dict = self.handle_finger(fmd5, fsha1, fsize)
                        path = code_dict["path"] + "/" + str(code_dict["id"])
                        if code_dict["code"] == 0:
                            try:
                                bou.put_object(path, response.content)
                            except:
                                time.sleep(3)
                                bou.put_object(path, response.content)
                        temp_list.append(path)
                    self.update_albums(str(temp_list), info)
                else:
                    print(info)

    def handle_finger(self, fmd5, fsha1, fsize, path="xqe/images"):
        conn = ConnMysql()
        ssql = """select count(*) from finger where fingermd5="%s" and fingersha1="%s";""" % (fmd5, fsha1)
        isql = """insert into finger (path,fingermd5,fingersha1,filesize) values ("%s","%s","%s",%s)""" % (path, fmd5, fsha1, fsize)
        esql = """select id,path from finger where fingermd5="%s" and fingersha1="%s";""" % (fmd5, fsha1)
        flag = conn.sql_select_one(ssql)
        if flag["count(*)"] == 0:
            conn.sql_change_msg(isql)
            res = conn.sql_select_one(esql)
            return {"code": 0, "id": res["id"], "path": res["path"]}
        else:
            res = conn.sql_select_one(esql)
            return {"code": 1, "id": res["id"], "path": res["path"]}

    def update_albums(self, img_url, info):
        conn = ConnMysql()
        sql = """insert into user_albums (albums_name,store_id,albums_href,img_url,other_msg) values ("%s","%s","%s","%s","%s");""" % (info["albums_name"], info["store_id"], info["albums_href"], img_url, info["other_msg"])
        conn.sql_change_msg(sql)

    def __del__(self):
        conn = ConnMysql()
        conn.release()

    def run(self):
        self.get_img_2_mysql()
        process_list = []
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
