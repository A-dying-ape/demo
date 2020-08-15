import oss2
import os


# 注意：一次只能操作一个bucket，如果要更换必须重新配置
BUCKET_INFO = {
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

# 基础路径
BASE_PATH = os.path.abspath(os.path.join(os.getcwd(), ".."))

# IP池
IP_POOL = [
    
   ]