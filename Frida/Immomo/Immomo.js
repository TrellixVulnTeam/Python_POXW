Java.perform(function () {
    console.log("Begin Javascript.");

    var doPostClass = Java.use("com.immomo.momo.protocol.a.b");
    doPostClass.doPost.overload('java.lang.String', 'java.util.Map').implementation = function (arg1, arg2) {
        if ("/log/uploadlocalapps" in arg1) {
            console.log("\n[*] arg1 -> " + arg1);

            console.log("[*] arg2 -> ");
            for (var i in arg2) {
                console.log("[*] arg2[" + i + "] -> " + arg2[i]);
            }
        }

        res = this.doPost(arg1, arg2);
        console.log("[*] this.doPost(arg1, arg2) -> " + res);
        return res;
    }


});