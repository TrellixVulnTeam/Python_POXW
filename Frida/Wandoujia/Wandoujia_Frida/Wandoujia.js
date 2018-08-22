Java.perform(function () {
    console.log("Begin Javascript.");

    var shareddata = Java.use("com.lib.common.sharedata.b");
    shareddata.a.overload('java.lang.String', 'int').implementation = function (str1, int1) {
        var res = this.a(str1, int1);
        console.log("\n[*] this.a(" + str1 + "," + int1 + ") -> " + res);
        return res
    }

    var PPJSCallUpIntentService = Java.use("com.pp.assistant.worker.PPJSCallUpIntentService");
    PPJSCallUpIntentService.onHandleIntent.implementation = function (arg1) {
        console.log("[*]  this.d ->" + this.d);
        var res = this.onHandleIntent(arg1);
        console.log("[*]  this.d ->" + this.d);
        return res
    }
});