#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: crypt.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/11/10 5:37 下午
# History:
#=============================================================================
"""
import abc
import base64
import hashlib
from typing import Optional

from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad


DEFAULT_BLOCK_SIZE = 8
DES_DEFAULT_PAD_LEN = DEFAULT_BLOCK_SIZE
AES_DEFAULT_BLOCK_SIZE = 32


class DecryptError(Exception):
    """解密异常"""
    pass


class CryptBase:
    def __init__(
        self,
        mode: int,
        key_string: bytes,
        key_salt: Optional[bytes] = None,
        key_iter: int = 1,
    ) -> None:
        self._mode = mode
        self._key_str = key_string
        self._key_salt = key_salt or b'\x00' * DEFAULT_BLOCK_SIZE
        self._key_iter = key_iter

    @abc.abstractmethod
    def _creator(self):  # type: ignore
        pass

    def _new_key(self) -> bytes:
        """
        转换加密的key
        步骤：
            - 加盐: new_key = key + slat
            - 循环计算md5：
                for _ in range(iter):
                    new_key = md5(new_key)
        """
        k = self._key_str + self._key_salt
        for _ in range(self._key_iter):
            k = hashlib.md5(k).digest()

        return k

    def encrypt(self, data: str, block_size: int = DEFAULT_BLOCK_SIZE) -> bytes:
        """
        加密
        :param data: 待加密的数据
        :param block_size: 块大小，默认8bytes
        :return:
        """
        # 每次都需要重新生成对象，否则会抛异常
        # TypeError: decrypt() cannot be called after encrypt()
        crypt_obj = self._creator()  # type: ignore
        crypt_text = base64.b64encode(crypt_obj.encrypt(pad(data_to_pad=data.encode('utf-8'), block_size=block_size)))
        return crypt_text

    def decrypt(self, data: str, block_size: int = DEFAULT_BLOCK_SIZE) -> bytes:
        """
        解密
        :param data: 待解密的数据
        :param block_size: 块大小，默认8bytes
        :return:
        """
        try:
            # 每次都需要重新生成对象，否则会抛异常
            # TypeError: decrypt() cannot be called after encrypt()
            crypt_obj = self._creator()  # type: ignore
            plain_text = unpad(padded_data=crypt_obj.decrypt(base64.b64decode(data)), block_size=block_size)
            return plain_text

        except Exception as e:
            raise DecryptError(e)


class DesCrypt(CryptBase):
    """DES 加解密"""

    def __init__(
        self,
        key_string: bytes,
        key_salt: Optional[bytes] = None,
        key_iter: int = 1,
        mode: int = DES.MODE_CBC
    ) -> None:
        """
        DES 加解密类
        :param key_string: des key
        :param key_salt: 盐
        :param key_iter: 秘钥的加密轮数
        :param mode: 加解密模式，默认为CBC方式
        """
        super(DesCrypt, self).__init__(mode=mode, key_string=key_string, key_salt=key_salt, key_iter=key_iter)

    def _creator(self):  # type: ignore
        """
        准备阶段，转换key，然后取计算后的md5前8位作为秘钥，秘钥位数为 64位
        """
        k = self._new_key()
        return DES.new(k[:8], self._mode, k[8:])


class AesCrypt(CryptBase):
    """AES 加解密"""

    def __init__(
        self,
        key_string: bytes,
        key_salt: Optional[bytes] = None,
        key_iter: int = 1,
        mode: int = AES.MODE_ECB
    ) -> None:
        """
        AES 加解密类
        :param key_string: aes key
        :param key_salt: 盐
        :param key_iter: 秘钥的加密轮数
        :param mode: 加解密模式，默认为ECB方式
        """
        super(AesCrypt, self).__init__(mode=mode, key_string=key_string, key_salt=key_salt, key_iter=key_iter)

    def _creator(self):  # type: ignore
        """
        准备阶段，转换key，以新key作为秘钥，秘钥位数为 256位
        """
        k = self._new_key()
        return AES.new(k, self._mode)

    def encrypt(self, data: str, block_size: int = AES_DEFAULT_BLOCK_SIZE) -> bytes:
        return super(AesCrypt, self).encrypt(data=data, block_size=block_size)

    def decrypt(self, data: str, block_size: int = AES_DEFAULT_BLOCK_SIZE) -> bytes:
        return super(AesCrypt, self).decrypt(data=data, block_size=block_size)
