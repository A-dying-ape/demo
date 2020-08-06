import oss2
from bucket.bucket_setting import mybucket_info
from itertools import islice


AKI = mybucket_info['access_key_id']
AKS = mybucket_info['access_key_secret']
BN = mybucket_info['bucket_name']
INT_INSIDER = mybucket_info['internal_endpoint']
INT_OUTSIDER = mybucket_info['intranet_endpoint']
INT_SPEEDUP = mybucket_info['speedup_endpoint']
PERMISSION = mybucket_info['permission']
AUTH = oss2.Auth(AKI, AKS)
BUCKET = oss2.Bucket(AUTH, INT_INSIDER, BN)


class uploadobj():
    def simpleupload(self, objname, uploadobj, islocalfile=False):
        """
        简单上传
        :param objname: str,bucket完整路径
        :param uploadobj: 上传的对象,可以是字符串,Bytes，Unicode,本地文件路径,网络流
        :islocalfile: True是本地文件
        :return: PutObjectResult <oss2.models.PutObjectResult>
        """
        if islocalfile:
            result = BUCKET.put_object_from_file(objname, uploadobj)
            return result
        else:
            result = BUCKET.put_object(objname, uploadobj)
            return result


class downloadobj():
    def downstream(self, objname, localfile):
        """
        下载到本地文件
        :param objname: str,bucket完整路径
        :param localfile: str,保存本地的文件路径
        :return: oss2.models.GetObjectResult
        """
        result = BUCKET.get_object_to_file(objname, localfile)
        return result


class showobj():
    def show_file(self, count=None, prefix=None):
        """
        列举文件
        :param count: 指定展示个数
        :param prefix: 指定前缀
        :return: 返回一个列表
        """
        if count is None:
            if prefix is None:
                return [b.key for b in oss2.ObjectIterator(BUCKET)]
            else:
                return [b.key for b in oss2.ObjectIterator(BUCKET, prefix=prefix)]
        else:
            if prefix is None:
                return [b.key for b in islice(oss2.ObjectIterator(BUCKET), count)]
            else:
                return [b.key for b in islice(oss2.ObjectIterator(BUCKET, prefix=prefix), count)]


class deleteobj():
    def delete_file(self, objectname=None, prefix=None):
        """
        删除文件
        :param objectname: bucket完整路径
        :param prefix: 前缀名
        :return: None
        """
        if objectname is None:
            objectname = []
        if prefix is None:
            if isinstance(objectname, list):
                try:
                    assert len(objectname) <= 1000
                except:
                    raise Exception("参数错误，每次只允许删除1000个！")
                else:
                    BUCKET.batch_delete_objects(objectname)
            elif isinstance(objectname, str):
                BUCKET.delete_object(objectname)
            else:
                print("一个还没有定义和处理的未知错误！")
        else:
            for obj in oss2.ObjectIterator(BUCKET, prefix=prefix):
                BUCKET.delete_object(obj.key)

