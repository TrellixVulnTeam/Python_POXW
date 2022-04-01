import base64
import hashlib
from typing import Any, Optional

from Crypto.Cipher import AES, DES

from loguru import logger


def pkcs5pad(text: str, pad_len: int = 8) -> bytes:
    tmp_pad_len = (pad_len - len(text) % pad_len) or pad_len
    padding = ''.join([chr(tmp_pad_len) for _ in range(0, tmp_pad_len)])
    return (text + padding).encode()


def pkcs5unpad(text: bytes, padlen: int = 8) -> bytes:
    def ord_func(c: Any):  # type: ignore
        return c if isinstance(c, (int, bytes)) else ord(c)

    if text:
        key = ord_func(text[-1])
        if padlen >= key > 0 and all(ord_func(x) == key for x in text[-key:]):
            text = text[:-key]
    return text


class DesHelper(object):
    def __init__(self, key_string: bytes, salt: Optional[bytes] = None, md5iter: int = 1) -> None:
        """
        :param key_string: 加密字符串
        :param salt: 盐
        :param md5iter: 加密轮数
        """
        self.key_str = key_string
        self.salt = salt or b'\x00' * 8
        self.md5iter = md5iter

    def prepare(self):  # type: ignore
        k = self.key_str + self.salt
        for i in range(self.md5iter):
            k = hashlib.md5(k).digest()
        return DES.new(k[:8], DES.MODE_CBC, k[8:])

    def encrypt(self, data: str) -> bytes:
        des = self.prepare()  # type: ignore
        secret = base64.b64encode(des.encrypt(pkcs5pad(data)))
        return secret

    def decrypt(self, data: str) -> bytes:
        try:
            des = self.prepare()  # type: ignore
            msg = pkcs5unpad(des.decrypt(base64.b64decode(data)))
            return msg
        except Exception as e:
            logger.exception(e)
            return b''


class AesHelper(object):
    def __init__(self, key_string: bytes, md5iter: int = 1) -> None:
        self.key_str = key_string
        self.md5iter = md5iter

    def prepare(self):  # type: ignore
        k = self.key_str
        for i in range(self.md5iter):
            k = hashlib.md5(k).hexdigest().encode()
        return AES.new(k, AES.MODE_ECB)

    def encrypt(self, data: str) -> bytes:
        aes = self.prepare()  # type: ignore
        secret = base64.b64encode(aes.encrypt(pkcs5pad(data, 16)))
        return secret

    def decrypt(self, data: str) -> bytes:
        try:
            aes = self.prepare()  # type: ignore
            msg = pkcs5unpad(aes.decrypt(base64.b64decode(data)), 16)
            return msg
        except Exception as e:
            logger.debug(e)
            return b''
