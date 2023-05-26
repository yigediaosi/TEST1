import base64
import json
import os
import sqlite3
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def load_local_key(localStateFilePath):
    "读取chrome保存在json文件中的key再进行base64解码和DPAPI解密得到真实的AESGCM key"
    with open(localStateFilePath, encoding='u8') as f:
        encrypted_key = json.load(f)['os_crypt']['encrypted_key']
    encrypted_key_with_header = base64.b64decode(encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def decrypt_value(key, data):
    "AESGCM解密"
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, cipherbytes, None).decode('u8')
    return plaintext


def fetch_host_cookie(host):
    "获取指定域名下的所有cookie"
    userDataDir = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data'
    localStateFilePath = userDataDir + r'\Local State'
    cookiepath = userDataDir + r'\Default\Cookies'
    # 97版本已经将Cookies移动到Network目录下
    if not os.path.exists(cookiepath) or os.stat(cookiepath).st_size == 0:
        cookiepath = userDataDir + r'\Default\Network\Cookies'
    # print(cookiepath)
    sql = f"select name,encrypted_value from cookies where host_key like '%.{host}'"
    cookies = {}
    key = load_local_key(localStateFilePath)
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        for name, encrypted_value in cu.execute(sql).fetchall():
            cookies[name] = decrypt_value(key, encrypted_value)
    return cookies


if __name__ == '__main__':
    print(fetch_host_cookie("anjuke.com"))
