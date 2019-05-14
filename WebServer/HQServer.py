"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : HQServer.py
 @Time    : 2019/4/18 10:22
"""
import json
from flask import Flask, request

app = Flask(__name__)

# 携程
# target_tel = "15968124907"    # 杨
# target_tel = "15655594670"      # 胡
# target_tel = "13666635816"
# target_tel = "18602807364"

# 小米云
# target_tel = 13588737491

# 去哪儿
# target_tel = "13666635816"
# target_tel = "18602807364"
# target_tel = "15655594670"

# 饿了么
target_tel = "15655594670"

APP_TYPE_TRIP = 20001  # 携程
APP_TYPE_QNE = 20002  # 去哪儿
APP_TYPE_XMC = 50004  # 小米云
APP_TYPE_ELM = 10005  # 饿了么


@app.route("/ics/task/getOneTask", methods=["GET"])
def GetOneTask():
    data = request.query_string
    print(data)

    # return json.dumps(dict(stateCode=0, data=dict(taskId="1", tel=target_tel, appType=APP_TYPE_TRIP)))
    # return json.dumps(dict(stateCode=0, data=dict(taskId="1", tel=target_tel, appType=APP_TYPE_XMC)))
    # return json.dumps(dict(stateCode=0, data=dict(taskId="1", tel=target_tel, appType=APP_TYPE_QNE)))
    return json.dumps(dict(stateCode=0, data=dict(taskId="1", tel=target_tel, appType=APP_TYPE_ELM)))


status_dict = {
    "200": "正在执行任务",
    "401": "爬虫设备异常",
    "700": "任务执行成功",
    "701": "任务执行失败"
}


@app.route("/ics/task/vm/update", methods=["GET"])
def UpdateStatus():
    data = request.query_string
    print(data)

    task_id = request.args.get("taskId")
    status = status_dict.get(request.args.get("status"), "")
    print("{task_id} is {status}".format(task_id=task_id, status=status))
    return json.dumps(dict(stateCode='0'))


@app.route("/ics/task/getPin", methods=["GET"])
def GetSMSCode():
    data = request.query_string
    print(data)

    sms = input("SMS Code -> ")
    return json.dumps(dict(stateCode='0', data=sms))


@app.route("/PassengerInfoEdit.aspx", methods=["POST"])
def PassengerInfoEdit():
    data = request.form
    cookies = request.cookies
    return json.dumps({"status": "ok"})


@app.route("/ics/task/resultFile", methods=["POST"])
def UploadSmallFile():
    data = request.form
    filename = data.get("fileName")

    files = request.files
    f = files[filename]
    f.save(filename)

    headers = request.headers

    return json.dumps(dict(stateCode=0))


@app.route("/ics/task/resultBigFile", methods=["POST"])
def UploadBigFile():
    data = request.form
    filename = data.get("fileName")
    offset = data.get("offset")

    files = request.files
    f = files[filename]
    f.save("{name}_{offset}".format(name = filename, offset = offset))
    return json.dumps(dict(stateCode=0))


app.run(host="0.0.0.0", port=13701, use_reloader=False, threaded=True)