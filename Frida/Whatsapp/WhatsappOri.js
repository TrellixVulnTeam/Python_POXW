Java.perform(function () {
    console.log("Begin Javascript.");

    var Exception = Java.use("java.lang.Exception");
    var log = Java.use("android.util.Log");

    var entrySerializableClass = Java.use("com.whatsapp.dns.DnsCacheEntrySerializable");
    entrySerializableClass.a.overload('java.lang.String').implementation = function (str1) {
        console.log("\n[*] entrySerializableClass.a!");
        console.log("[*] str1 -> " + str1);

        console.log(log.getStackTraceString(Exception.$new()));
        // throw Exception.$new("Whatsapp Exception...");
        return this.a(str1);
    };

    // entrySerializableClass.$init.overload('java.lang.Long', 'java.net.InetAddress', 'int').implementation = function (arg1, arg2, arg3) {
    //     console.log("\n[*] entrySerializableClass.$init!");
    //     console.log("[*] arg1 -> " + arg1);
    //     console.log("[*] arg2 -> " + arg2);
    //     console.log("[*] arg3 -> " + arg3);
    //
    //     return this.$init(arg1, arg2, arg3)
    // };

    var messagingG = Java.use("com.whatsapp.messaging.g");
    messagingG.$init.implementation = function (arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8) {
        console.log("\n[*] messagingG.$init!");
        console.log("[*] arg1 -> " + arg1);
        console.log("[*] arg2 -> " + arg2);
        console.log("[*] arg3 -> " + arg3);
        console.log("[*] arg4 -> " + arg4);
        console.log("[*] arg5 -> " + arg5);
        console.log("[*] arg6 -> " + arg6);
        console.log("[*] arg7 -> " + arg7);
        console.log("[*] arg8 -> " + arg8);

        console.log(log.getStackTraceString(Exception.$new()));
        return this.$init(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)
    };

    messagingG.a.overload().implementation = function () {
        console.log("\n[*] messagingG.a!");
        console.log("this.b -> " + this.b.value);
        console.log("this.l -> " + this.l.value);
        console.log("this.m -> " + this.m.value);

        console.log(log.getStackTraceString(Exception.$new()));
        return this.a()
    };

    var dnsC = Java.use("com.whatsapp.dns.c");
    dnsC.a.overload('java.lang.String', 'java.lang.Iterable', 'int').implementation = function (arg1, arg2, arg3) {
        console.log("\n[*] dnsC.a!");
        console.log("[*] arg1 -> " + arg1);
        console.log("[*] arg2 -> " + arg2);
        console.log("[*] arg3 -> " + arg3);

        console.log(log.getStackTraceString(Exception.$new()));
        return this.a(arg1, arg2, arg3);
    };

});