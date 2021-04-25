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
import hashlib, secrets, binascii

from tinyec import registry

from Crypt.AES import AesCrypt


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()


curve = registry.get_curve('brainpoolP256r1')


def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)

    _aes = AesCrypt(secretKey)
    ciphertext = _aes.encrypt(msg)
    return (ciphertext, ciphertextPrivKey * curve.g)


def decrypt_ECC(ciphertext,ciphertextPubKey, privKey):
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)

    _aes = AesCrypt(secretKey)
    plaintext = _aes.decrypt(ciphertext)
    return plaintext


msg = 'Text to be encrypted by ECC public key and ' \
      'decrypted by its corresponding ECC private key'
print("original msg:", msg)
privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g

ciphertext, ciphertextPubKey = encrypt_ECC(msg, pubKey)
print(f"encrypted msg: {ciphertext=}\n{ciphertextPubKey=}\n\n")

decryptedMsg = decrypt_ECC(ciphertext, ciphertextPubKey, privKey)
print("decrypted msg:", decryptedMsg)
