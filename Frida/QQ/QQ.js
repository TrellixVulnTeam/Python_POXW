Java.perform(function () {
    console.log("Begin Javascript.");

    var TbsDownloader = Java.use("com.tencent.smtt.sdk.TbsDownloader");
    TbsDownloader.readResponse.overload('java.lang.String', 'int', 'boolean', 'boolean', 'boolean').implementation = function (str1, int1, b1, b2, b3) {
        var res = this.readResponse(str1, int1, b1, b2, b3);
        console.log("\n[*] str -> " + str1);
        return res
    }
});