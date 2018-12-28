Java.perform(function () {
    console.log("Begin Javascript.");

    var Exception = Java.use("java.lang.Exception");
    var log = Java.use("android.util.Log");

    var entrySerializableClass = Java.use("com.whatsapp.dns.DnsCacheEntrySerializable");
    entrySerializableClass.a.overload('java.lang.String').implementation = function (str1) {
        console.log("\n[*] entrySerializableClass.a!");
        console.log("[*] str1 -> " + str1);
        send(str1);
        // console.log(log.getStackTraceString(Exception.$new()));
        // throw Exception.$new("Whatsapp Exception...");
        return this.a(str1);
    };
});