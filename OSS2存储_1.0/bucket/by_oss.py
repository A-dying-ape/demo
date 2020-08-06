from bucket.bucket_setting import *
from oss2.models import *

AKI = mybucket_info['access_key_id']
AKS = mybucket_info['access_key_secret']
BN = mybucket_info['bucket_name']
INT_INSIDER = mybucket_info['internal_endpoint']
INT_OUTSIDER = mybucket_info['intranet_endpoint']
INT_SPEEDUP = mybucket_info['speedup_endpoint']
PERMISSION = mybucket_info['permission']
headers = headers


class OSS_Bucket_Manage():
    """bucket基础管理"""
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)
        self.service = oss2.Service(self.auth, self.endpoint)

    def create_bucket(self):
        """
        :return: None
        """
        if self.does_bucket_exist():
            print("创建的%s已存在！是否命名重复？" % BN)
        else:
            self.bucket.create_bucket(PERMISSION)

    def show_buckets(self, prefix=None, marker=None):
        """
        :param prefix: 指定前缀
        :param marker: 指定某个存储空间
        :return: 返回一个列表
        """
        return [b.name for b in oss2.BucketIterator(self.service, prefix=prefix, marker=marker)]

    def does_bucket_exist(self):
        """
        :return: 布尔值
        """
        try:
            self.bucket.get_bucket_info()
        except oss2.exceptions.NoSuchBucket:
            return False
        except:
            raise
        return True

    def get_bucket_info(self):
        """
        :return: 名称，存储类型，创建时间，内网域名，外网域名，用户ID，ACL权限，数据容灾类型，地域信息
        """
        if self.does_bucket_exist():
            bucket_info = self.bucket.get_bucket_info()
            return {
                "名称":bucket_info.name,
                "存储类型":bucket_info.storage_class,
                "创建时间":bucket_info.creation_date,
                "内网域名":bucket_info.intranet_endpoint,
                "外网域名":bucket_info.extranet_endpoint,
                "用户ID":bucket_info.owner.id,
                "ACL权限":bucket_info.acl.grant,
                "数据容灾类型":bucket_info.data_redundancy_type,
                "地域信息":bucket_info.location
            }
        else:
            return "所查存储信息对应的%s不存在！" % BN

    def delete_bucket(self):
        """
        :return: None
        """
        if self.does_bucket_exist():
            try:
                self.bucket.delete_bucket()
            except oss2.exceptions.BucketNotEmpty:
                print("%s不为空！可以通过边列举边删除(对于分片上传则是终止上传)的方法清空存储空间,然后再删除。" % BN)
        else:
            print("%s不存在！检查是否已经创建？" % BN)


class OSS_Bucket_ACL():
    """权限管理"""
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)

    def set_bucket_acl(self):
        """
        设置bucket访问权限(服务器拥有者才有权限)
        :return: None
        """
        self.bucket.put_bucket_acl(PERMISSION)

    def get_bucket_acl(self):
        """
        获取bucket访问权限
        :return: 返回权限值
        """
        return self.bucket.get_bucket_acl().acl


class OSS_Bucket_Tagging():
    """bucket标签设置"""
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)
        self.service = oss2.Service(self.auth, self.endpoint)

    def set_bucket_tag(self):
        """
        :return: 返回状态码，200表示成功
        """
        rule = TaggingRule()
        for k, v in tag_rule.items():
            rule.add(k, v)
        tagging = Tagging(rule)
        return self.bucket.put_bucket_tagging(tagging).status

    def get_bucket_tag(self):
        """
        :return: 所有bucket标签
        """
        return self.bucket.get_bucket_tagging().tag_set.tagging_rule

    def delete_bucket_tag(self):
        """
        :return: 返回状态码，200表示成功
        """
        return self.bucket.delete_bucket_tagging().status

    def show_buckets_by_tag(self):
        """
        :return: 返回一个列表
        """
        return [tn.name for tn in self.service.list_buckets(params=params).buckets]


class OSS_Bucket_Policy():
    """授权策略配置"""
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)

    def set_bucket_policy(self):
        """
        :return: None
        """
        self.bucket.put_bucket_policy(policy_text)

    def get_bucket_policy(self):
        """
        :return: 返回json字符串
        """
        return json.loads(self.bucket.get_bucket_policy().policy)

    def delete_bucket_policy(self):
        """
        :return: None
        """
        result = self.bucket.delete_bucket_policy()
        try:
            assert int(result.status) // 100 == 2
        except:
            print("删除失败！")


class OSS_Bucket_Request_Payment():
    """请求者付费模式"""
    def __init__(self):
        self.endpoint = INT_INSIDER
        self.auth = oss2.Auth(AKI, AKS)
        self.bucket = oss2.Bucket(self.auth, self.endpoint, BN)

    def set_bucket_request_payment(self, flag=False):
        """
        :param: flag开关
        :return: 状态码，200表示成功
        """
        if flag:
            result = self.bucket.put_bucket_request_payment(PAYER_BUCKETOWNER)
            print("关闭请求者付费模式！")
        else:
            result = self.bucket.put_bucket_request_payment(PAYER_REQUESTER)
            print("打开请求者付费模式！")
        return result.status

    def get_bucket_request_payment(self):
        """
        :return: 请求者付费模式配置
        """
        return self.bucket.get_bucket_request_payment().payer

    def put_object(self, object_name):
        """
        :param object_name: 要上传的文件
        :return: 状态码
        """
        return self.bucket.put_object(object_name, 'test-content', headers=headers)

    def delete_object(self, object_name):
        """
        :param object_name:  要删除的文件
        :return: 状态码
        """
        return self.bucket.delete_object(object_name, headers=headers)



