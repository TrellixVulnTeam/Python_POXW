Java.perform(function () {
    var launcher = Java.use("com.tencent.mm.ui.LauncherUI");
    launcher.onCreate.implementation = function (bundle) {
        send(bundle.toString());
        var ret = this.onCreate(bundle);
        // send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
        return ret;
    };
    // send(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
});
