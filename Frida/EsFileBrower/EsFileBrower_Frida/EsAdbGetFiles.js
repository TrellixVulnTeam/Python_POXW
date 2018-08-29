Java.perform(function () {
    console.log("Begin Javascript.");

    // estrong 获取手机信息js测试
    var adbControlClass = Java.use("com.estrongs.android.pop.app.AdbControllerActivity");
    adbControlClass.onCreate.implementation = function (arg1) {
        for (arg in arg1) {
            console.log("\n[*] arg1[" + arg + "] = " + arg1[arg])
        }

        var adbRemoteIp = this.getIntent().getExtras().getString("adbRemoteIp");
        var adbControlMode = this.getIntent().getExtras().getString("adbControlMode");

        console.log("[*] adbRemoteIp -> " + adbRemoteIp);
        console.log("[*] adbControlMode -> " + adbControlMode);

        return this.onCreate(arg1)
    };

    var jsonClass = Java.use("com.estrongs.android.f.c");
    // jsonClass.h.overload('com.estrongs.android.f.c').implementation = function (arg1) {
    //     console.log("\n[*] Begin overload(com.estrongs.android.f.c)");
    //
    //     var res =  this.h(arg1);
    //     console.log("\n[*] res -> " + res);
    //     console.log("[*] JsonData -> " + JSON.stringify(res));
    //
    //     return res
    // };

    jsonClass.h.overload().implementation = function () {
        console.log("\n[*] Begin overload()");

        var res =  this.h();

        for (var i in res){
            console.log("[*] res[" + i + "] = " + res[i])
        }


        // console.log("\n[*] res -> " + res);
        // console.log("[*] JsonData -> " + JSON.stringify(res));

        return res
    };

    var commonGetClass = Java.use("com.estrongs.android.f.a");
    commonGetClass.a.overload('java.lang.String', 'java.lang.String', 'java.util.Properties', 'java.util.Properties', 'java.util.Properties').implementation = function (str1, str2, properties1, properties2, properties3) {
        console.log("\n[*] str1 -> " + str1);
        console.log("[*] str2 -> " + str2);
        console.log("[*] properties1 -> " + properties1);
        console.log("[*] properties2 -> " + properties2);
        console.log("[*] properties3 -> " + properties3);

        console.log("[*] JsonData -> " + JSON.stringify(jsonClass.j));

        res = this.a(str1, str2, properties1, properties2, properties3);
        console.log("[*] res -> " + res);

        return res
    }

    var CreateOAuthNetDiskClass = Java.use("com.estrongs.android.ui.view.CreateOAuthNetDisk")
    CreateOAuthNetDiskClass.a.overload('java.util.Properties').implementation = function (Properties) {
        console.log("\n[*] Properties -> " + Properties);
        console.log("[*] this.m -> " + this.m);

    }

    // es 上传测试
    // var estrongPostClass = Java.use("com.estrongs.a.b.d");
    // estrongPostClass.a.overload('java.io.InputStream').implementation = function (inputStream) {
    //     // console.log("\n[*] inputStream -> " + inputStream);
    //
    //     var res = this.a(inputStream);
    //     console.log("[*] com.estrongs.a.b.d.a(InputStream) -> " + res);
    //     return res;
    // }
    //
    // var uClass = Java.use("com.estrongs.fs.b.u");
    // uClass.a.overload('[B', 'java.lang.String').implementation = function (byte1, str1) {
    //     console.log("\n[*] byte1 -> " + byte1);
    //     console.log("[*] str1 -> " + str1);
    //
    //     var res = this.a(byte1, str1);
    //     console.log("[*] com.estrongs.fs.b.u.a(byte1, str1) -> " + res);
    //     return res;
    // }

});