"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FeedbackServer.py
 @Time    : 2018/10/10 14:59
"""
import json
from flask import Flask, send_file, send_from_directory, make_response, request, redirect, url_for
from Crypt.AES import AES_ECB_DECRYPT,AES_ECB_ENCRYPT, md5

app = Flask(__name__)


@app.route("/Data/Upload", methods=["POST"])
def DataUpload():
    data = request.data

    deviceId = request.args.get("device")
    randomChr = request.args.get("rnd")
    key = md5(md5(deviceId + randomChr)).encode()
    plaintext = AES_ECB_DECRYPT(data, key)
    print(plaintext)

    return AES_ECB_ENCRYPT(json.dumps(dict(isSuccess="true", type="Im")).encode(), key)


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
