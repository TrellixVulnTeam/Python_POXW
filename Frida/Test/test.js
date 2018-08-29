Java.perform(function () {
    console.log("Begin Javascript.");

    var targetClass = Java.use("com.yxcorp.gifshow.log.k");
    targetClass.a.overload('java.lang.String', 'java.lang.String', '[Ljava.lang.Object;').implementation = function (arg1, arg2, arg3) {
        console.log("\n[*] arg1 -> " + arg1);
        console.log("[*] arg2 -> " + arg2);
        console.log("[*] arg3 -> " + arg3);

        res = this.a(arg1, arg2, arg3);
        console.log("[*] this.a(arg1, arg2, arg3) -> " + res);
        return res;
    }

    targetClass.a.overload('boolean', 'java.lang.String', 'java.lang.String', 'java.util.Map', 'boolean').implementation = function (arg1, arg2, arg3, arg4, arg5) {
        console.log("\n[*] arg1 -> " + arg1);
        console.log("[*] arg2 -> " + arg2);
        console.log("[*] arg3 -> " + arg3);
        console.log("[*] arg4 -> " + arg4);
        console.log("[*] arg5 -> " + arg5);

        res = this.a(arg1, arg2, arg3, arg4, arg5);
        console.log("[*] this.a(arg1, arg2, arg3,arg4, arg5)  -> " + res);
        return res;
    }

    var targetClass2 = Java.use("com.yxcorp.gifshow.log.SystemInfoCollector");
    targetClass2.a.overload('java.lang.String').implementation = function (arg1) {
        console.log("\n[*] arg1 -> " + arg1);

        res = this.a(arg1);
        console.log("[*] this.a(arg1) -> " + res);
        return res;
    }

});