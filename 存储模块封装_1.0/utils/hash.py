"""
对接收的内容进行指纹处理
"""
import hashlib


def md5hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.hexdigest()

def sha1hash(content):
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()