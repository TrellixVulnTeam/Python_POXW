#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: ECC.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/4/17 1:53 下午
# History:
#=============================================================================
"""
import hashlib
import random
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

from Crypt.AES import AesCrypt


def ecc_point_to_256_bit_key(point:ECC.EccPoint):
    sha = hashlib.sha256(int.to_bytes(int(point.x), 32, 'big'))
    sha.update(int.to_bytes(int(point.y), 32, 'big'))
    return sha.digest()


def encrypt_ECC(msg, pubKey: ECC.EccKey):
    cipher_private_key = random.randint(1, pubKey._curve.order)
    sharedECCKey = cipher_private_key * pubKey.pointQ
    aes_key = ecc_point_to_256_bit_key(sharedECCKey)

    _aes = AesCrypt(aes_key)
    ciphertext = _aes.encrypt(msg)
    return (ciphertext, cipher_private_key * pubKey.pointQ)


def decrypt_ECC(ciphertext, cipher_text_public_key, private_key: ECC.EccKey):
    sharedECCKey = private_key.d * cipher_text_public_key
    aes_key = ecc_point_to_256_bit_key(sharedECCKey)

    _aes = AesCrypt(aes_key)
    plaintext = _aes.decrypt(ciphertext)
    return plaintext


msg = 'Text to be encrypted by ECC public key and ' \
      'decrypted by its corresponding ECC private key'
print("original msg:", msg)

private_key = ECC.generate(curve='P-256')
public_key = private_key.public_key()

cipher_text, cipher_text_public_key = encrypt_ECC(msg, public_key)
print(f"encrypted msg: {cipher_text=}\n{cipher_text_public_key=}\n\n")

decryptedMsg = decrypt_ECC(cipher_text, cipher_text_public_key, private_key)
print("decrypted msg:", decryptedMsg)
