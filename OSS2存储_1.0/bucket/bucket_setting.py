import oss2
from oss2.headers import OSS_REQUEST_PAYER


# 注意：一次只能操作一个bucket，如果要更换必须重新配置
mybucket_info = {
    # 访问密钥
    "access_key_id":"",
    "access_key_secret":"",
    # OSS存储空间名称
    "bucket_name":"",
    # 传输协议
    "schema":"https",
    # 外网访问域名
    "internal_endpoint":"oss-cn-shanghai.aliyuncs.com",
    # 内网访问域名
    "intranet_endpoint":"oss-cn-shanghai-internal.aliyuncs.com",
    # 传输加速访问域名
    "speedup_endpoint":"oss-accelerate.aliyuncs.com",
    # 读写权限
    # oss2.BUCKET_ACL_PRIVATE  私有的，只有拥有者有权限
    # oss2.BUCKET_ACL_PUBLIC_READ  公共读的，拥有者可以读写，其他人只能读
    # oss2.BUCKET_ACL_PUBLIC_READ_WRITE  公共读写，任何人都可以读写
    "permission":oss2.BUCKET_ACL_PUBLIC_READ,
}

# 最多可设置20对Bucket用户标签(Key-Value对)，且编码必须是UTF-8。
# key:最大长度为64字节，不能以http ://、https://、Aliyun为前缀，且不能为空。
# value:Value最大长度为128字节，可以为空。
tag_rule = {
    # "key":"value"

}

params = {
    # "tag-key": tagging_rule中的key,
    # "tag-value": tagging_rule中的value

}

# 配置授权策略
# policy_text = '{"Statement": [{"Effect": "Allow", "Action": ["oss:GetObject", "oss:ListObjects"], "Resource": ["acs:oss:*:*:*/user1/*"]}], "Version": "1"}'
policy_text = ''

# 第三方付费访问请求头
headers = {
    OSS_REQUEST_PAYER: "requester"
}

ip_pool = [
    
   ]