Java.perform(function () {
    console.log("[*] Script start.")
    var sysExitClass = Java.use("java.lang.System")
    sysExitClass.exit.implementation = function () {
        console.log("[*] System.exit called.")
    };

    // var strnmapAddress = undefined;
    // Module.enumerateImports("libfoo.so", {
    //     onMatch: function (imp) {
    //         if (imp.name === "strncmp") {
    //             strnmapAddress = imp.address;
    //             console.log("strnmapAddress: ", strnmapAddress)
    //         }
    //     },
    //     onComplete: function () {
    //     }
    // });

    // Interceptor.attach(strnmapAddress,{
    // 在真机Android 7.0上会提示错误 “Error: unable to intercept function at 0xaa1e20c7; please file a bug”
    Interceptor.attach(Module.findExportByName("libfoo.so", "strncmp"), {
        onEnter: function (args) {
            console.log(args[0]);
            console.log(args[1]);
            console.log(args[2]);
            if (args[2].toInt32() == 23 && Memory.readUtf8String(args[0], 23) == "01234567890123456789012") {
                console.log("[*] Secret string at " + args[1] + ": " + Memory.readUtf8String(args[1], 23));
            }
        },
        onLeave: function (retval) {
        }
    });
});