#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: RSA.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/4/22 8:08 下午
# History:
#=============================================================================
"""

import pathlib

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP

from Crypt.AES import AesCrypt


def ras_encrypt(
    public_key_file: pathlib.Path,
    plain_text: str
) -> str:
    """
    ras 加密
    :param public_key_file: ras 公钥文件
    :param plain_text: 待加密的内容
    :return:
    """
    assert public_key_file.exists(), FileNotFoundError(f"RSA公钥文件{public_key_file}不存在")

    # 生成随机的aes密钥
    aes_session_key = get_random_bytes(16)

    # 使用rsa公钥加密aes密钥
    public_key = RSA.import_key(public_key_file.read_bytes())
    rsa_cipher = PKCS1_OAEP.new(public_key)
    aes_encrypt_session_key = rsa_cipher.encrypt(aes_session_key)

    # 使用aes秘钥加密明文
    aes_cipher = AesCrypt(aes_session_key)
    cipher_text = aes_cipher.encrypt(plain_text)

    # 返回组合后的密文联合体
    return f"{aes_encrypt_session_key.hex()[::-1]}g{cipher_text.hex()[::-1]}"


def rsa_decrypt(
    private_key_file: pathlib.Path,
    union_cipher_text: str
) -> str:
    """
    ras 解密
    :param private_key_file: rsa 私钥文件
    :param union_cipher_text: 待解密的密文联合体
    :return:
    """
    assert private_key_file.exists(), FileNotFoundError(f"RSA私钥文件{private_key_file}不存在")

    # 分离密文联合体
    aes_encrypt_session_key, cipher_text = union_cipher_text.split('g')
    aes_encrypt_session_key = bytes.fromhex(aes_encrypt_session_key[::-1])
    cipher_text = bytes.fromhex(cipher_text[::-1])

    # 使用rsa私钥解出aes公钥
    private_key = RSA.import_key(private_key_file.read_text())
    rsa_cipher = PKCS1_OAEP.new(private_key)
    aes_session_key = rsa_cipher.decrypt(aes_encrypt_session_key)

    # 使用aes公钥进行解密
    aes_cipher = AesCrypt(aes_session_key)
    return aes_cipher.decrypt(cipher_text.decode()).decode()


if __name__ == '__main__':
    print(rsa_decrypt(private_key_file=pathlib.Path("./id_rsa"), union_cipher_text="572572697b0bf898fe0767ff65ab13b9626fc66013f3b554c5cf63329e53c665111c152b760840f1c0dbbb7814c0bda6e773f7b2a766be7e59bee970df477ed153f0d0dab4ae632d0456e093d05cf0520aa277056f9e199b76343122e0f8ba91da6ff5b381f31afbb0cd53dd2a1ac990bd94f717203fd54f9ef34cf5d32980584bdd98a64c292460f5512fc625fdf66f22d8cc6a5d66e48ca8c023770f070ec3f037f14863802850dce7e708a1868707e4617700f75666a0b5fdfbd84482306735cfc9665c317595765d28ddbaca20c7efb02c2e162083a1ffe0a9e78ae19fe62747af93990fa10391ddf2c208f7fb4eeea7780d3f99348e70c635724ca977a3gd3d31437c603e4140766d44785146396263734f284033703f6561353c4630724a4f47527856523947403e676a6459463e467f644959473c425077793b273b62635b6847474a4a726b2b2162763c444454625379354463533"))
