console.log("[*]Script begin.");

Java.perform(function () {
    // 修改onClick的实现，使得点击ok后进程不退出
    var bClass = Java.use("sg.vantagepoint.uncrackable1.b");
    bClass.onClick.implementation = function (arg1, arg2) {
        console.log("[*] onClick called")
    };

    // Bytes数组转换成String
    function ByteToString(byteList) {
        var str_a = "";
        for (var i = 0; i < byteList.length; i++) {
            str_a += String.fromCharCode(byteList[i]);
        }
        return str_a;
    }

    // 修改实现，打印出正确的输入函数
    var aClass = Java.use("sg.vantagepoint.a.a");
    aClass.a.implementation = function (arg1, arg2) {
        console.log("[*]Inside begin.");
        var ret_value = this.a(arg1, arg2);
        console.log("[*]Right password: " + ByteToString(ret_value));       // 转码后打印在控制台
        return ret_value;
    }
});