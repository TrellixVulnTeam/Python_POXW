import base64
import hashlib
from typing import Tuple

from Crypto.PublicKey import RSA

from .aes import AesHelper

Base64DecodeError = Exception

AES_KEY_STRING = b"bw+6ySkUOhmFnzN3xOMwYQ=="
aes = AesHelper(AES_KEY_STRING)


def generate_key_pair(bits: int = 2048) -> Tuple[bytes, bytes]:
    """
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    """
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("OpenSSH")
    private_key = new_key.exportKey("PEM")
    RSA.importKey(private_key)
    return public_key, private_key


def generate_pubkey_from_private_key(private_key_str: str) -> bytes:
    """
    传入私钥，返回公钥
    :param private_key_str: 私钥字符串
    :return: 公钥字符串
    """
    private_key = RSA.importKey(private_key_str)
    pub_key = private_key.publickey()
    pub_str = pub_key.exportKey("OpenSSH")
    return pub_str


def encrypt_string(data: str) -> str:
    """
    加密字符串
    :param data: 带加密的字符串
    :return: 加密后的字符串
    """
    return aes.encrypt(data).decode() if data else data


def decrypt_string(data: str) -> str:
    """
    解密字符串，如果解密失败，返回原字符串, 这是为了给解密password时提供编程方便
    比如: password = decrypt_string(password)
    :param data: 加密的字符串
    :return: 解密后的结果
    """
    result = aes.decrypt(data)
    return result.decode(errors='ignore') or data


def base64_encode(string: bytes) -> bytes:
    """
    对字符串进行base64加码
    :param string: str 要加码的字符串
    :return 加码后的字符串
    """
    encode_base64_string = base64.b64encode(string)
    return encode_base64_string


def base64_decode(string: str) -> bytes:
    """
    对字符串进行base64解码
    :param string: str 要解码的字符串
    :return 解码后的字符串
    :raise Base64DecodeError 解码base64失败了
    """
    try:
        decode_base64_string = base64.b64decode(string)
        return decode_base64_string
    except Exception:
        # 前端可能存在漏掉加密的情况，此时抛出异常
        raise Base64DecodeError()


# def _read_chunks(fh):
#     fh.seek(0)
#     chunk = fh.read(8096)
#     while chunk:
#         yield chunk
#         chunk = fh.read(8096)
#     else:
#         fh.seek(0)


def md5sum(source: bytes) -> str:
    """
    md5值计算
    :param source: 为字符串时，如果这个字符串表示文件(路径存在)，则计算该文件，否则计算字符串的md5;
                   若为文件流，则计算该文件的md5
    :return:
    """
    m = hashlib.md5()
    m.update(source)
    return m.hexdigest()

# class SSH_Key:
#     pub_private = {}
#
#     @classmethod
#     def get_pub_from_private(cls, private_key):
#         return generate_pubkey_from_private_key(private_key)
#
#     @classmethod
#     def get_pub_from_cache(cls, private_key):
#         return cls.pub_private.get(private_key, None)
#
#     @classmethod
#     def get_private_key_from_pub(cls, pub_key):
#         private_key = cls.pub_private.get(pub_key)
#         if not private_key:
#             raise Exception("can not get private key from pub key")
#         else:
#             return private_key
#
#     @classmethod
#     def clear_key(cls, pub_key):
#         if pub_key in cls.pub_private:
#             cls.pub_private.pop(pub_key)
#
#     @classmethod
#     def generate_key_pair(cls):
#         pub_key, private_key = generate_key_pair()
#         cls.pub_private[pub_key] = private_key
#         return pub_key
