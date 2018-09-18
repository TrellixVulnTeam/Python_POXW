"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : WifiCrackServerTest.py
 @Time    : 2018/9/6 16:51
"""
import json
import random
from flask import Flask, request

app = Flask(__name__)


@app.route("/device/commit/password", methods=['POST'])
def UploadPassword():
    data = request.form.to_dict()
    print(data)
    return json.dumps(dict(code=0))


@app.route("/task/add", methods=['POST'])
def TaskAdd():
    data = request.form.to_dict()
    print(data)
    taskId = random.randint(1, 100)
    return json.dumps(dict(code=0, taskId=taskId))  # 成功
    # return json.dumps(dict(code=1, msg="error"))  # 失败


@app.route("/task/getCrackResult/<taskid>", methods=['GET'])
def GetCrackResult(taskid):
    data = request.form.to_dict()
    print(taskid, data)
    # return json.dumps(dict(code=0, password="12345678"))    # 成功
    return json.dumps(dict(code=2, msg="no password"))  # 失败


@app.route("/task/cancel/<id>", methods=['GET'])
def TaskCancel(id):
    data = request.form.to_dict()
    print("TaskCancel: ", id, data)
    return json.dumps(dict(code=0))


@app.route("/device/getCrackNumber/<id>", methods=['GET'])
def TaskGetCrackNumber(id):
    data = request.form.to_dict()
    print("GetCrackNumber: ", id, data)
    return json.dumps(dict(code=0, userDistributeCount=100, userDistributeUsedCount=0))


@app.route("/task/getCrackResult/", methods=['GET'])
def TaskGetCrackResult():
    data = request.form.to_dict()
    print("GetCrackResult: ", data)
    return json.dumps(dict(code=2))


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
