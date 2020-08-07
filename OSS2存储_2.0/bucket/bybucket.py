import oss2
from bucket.bsetting import mybucket_info
from itertools import islice


AKI = mybucket_info['access_key_id']
AKS = mybucket_info['access_key_secret']
BN = mybucket_info['bucket_name']
INT_INSIDER = mybucket_info['internal_endpoint']
INT_OUTSIDER = mybucket_info['intranet_endpoint']
INT_SPEEDUP = mybucket_info['speedup_endpoint']
PERMISSION = mybucket_info['permission']


class Bucket_Obj_Upload(object):
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)

    def upload_file(self, objectname, localfile):
        """
        上传文件到指定bucket
        :param objectname: 上传oss完整路径
        :param localfile: 本地路径
        :return: None
        """
        self.bucket.put_object_from_file(objectname, localfile)

    def put_object(self, object_name, input):
        """
        :param object_name: 上传的文件名
        :param input: 网络流(可迭代)
        :return: 状态码
        """
        return self.bucket.put_object(object_name, input)

    def download_file(self, objectname, localfile):
        """
        下载指定bucket里的某个文件
        :param objectname: 上传oss完整路径
        :param localfile: 本地路径
        :return: None
        """
        self.bucket.get_object_to_file(objectname, localfile)

    def show_file(self, count):
        """
        展示指定bucket下的所有文件
        :param count: 指定展示个数
        :return: 返回一个列表
        """
        return [b.key for b in islice(oss2.ObjectIterator(self.bucket), count)]

    def delete_file(self, objectname=None, prefix=None):
        """
        删除指定某个bucket下的某个文件，某批文件，以某个前缀开头的文件
        :param objectname: 上传oss完整路径
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
                    self.bucket.batch_delete_objects(objectname)
            elif isinstance(objectname, str):
                self.bucket.delete_object(objectname)
            else:
                print("一个还没有定义和处理的未知错误！")
        else:
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
                self.bucket.delete_object(obj.key)
