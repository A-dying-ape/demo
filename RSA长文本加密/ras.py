from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import os


def create_pem():
    # 生成秘钥 1024
    rsa = RSA.generate(1024)
    if os.path.exists("./pem"):
        print("密匙和密钥已经存在在D盘下的pem文件夹中")
    else:
        os.mkdir("./pem")
        with open('./pem/private.pem', mode='wb') as f:
            f.write(rsa.export_key())
        with open('./pem/public.pem', mode='wb') as f:
            f.write(rsa.publickey().export_key())


def get_txt_name():
    # 要加密的文本都放到源文本目录下
    files_name = os.listdir("./源文本")
    return files_name


def encrypt(text, file, length=100):
    # 加载秘钥, 使用公钥进行加密
    pub_key = open('./pem/public.pem').read()
    key = RSA.import_key(pub_key)
    # 生成加密对象
    cipher = PKCS1_v1_5.new(key)
    result = b""
    for i in range(0, len(text), length):
        encode_rsa_data = cipher.encrypt(text[i: i+length])
        b64_data = base64.b64encode(encode_rsa_data)
        result += b64_data
    if os.path.exists("./加密后的文本"):
        with open("./加密后的文本/" + file, "wb") as f:
            f.write(result)
    else:
        os.mkdir("./加密后的文本")
        with open("./加密后的文本/" + file, "wb") as f:
            f.write(result)


def decrypt(text, file, length=172):
    # 1. 加载秘钥
    pri_key = open('./pem/private.pem').read()
    # 2. 实例化一个秘钥对象
    key = RSA.import_key(pri_key)
    # 3. 获取一个 rsa 对象
    rsa = PKCS1_v1_5.new(key)
    result = b""
    for i in range(0, len(text), length):
        data = base64.b64decode(text[i: i+length])
        decode_rsa_data = rsa.decrypt(data, b'rsa')
        result += decode_rsa_data
    if os.path.exists("./解密后的文本"):
        with open("./解密后的文本/" + file, "wb") as f:
            f.write(result)
    else:
        os.mkdir("./解密后的文本")
        with open("./解密后的文本/" + file, "wb") as f:
            f.write(result)


if __name__ == '__main__':
    # 自动生成密钥密匙
    create_pem()

    #读取文本目录
    files_name = get_txt_name()

    # 读取文本内容进行加密
    for file in files_name:
        with open("./源文本/" + file, "rb") as f1:
            enc_text = f1.read()
        encrypt(enc_text, file)

    # 读取密文文本进行解密
    for file in files_name:
        with open("./加密后的文本/" + file, "rb") as f2:
            dec_text = f2.read()
        decrypt(dec_text, file)



