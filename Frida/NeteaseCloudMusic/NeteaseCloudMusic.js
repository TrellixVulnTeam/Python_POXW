Java.perform(function () {
    console.log("Begin Javascript.");

    var targetClass = Java.use("com.netease.cloudmusic.b.a.a");
    targetClass.b.overload('java.util.List', 'java.lang.String').implementation = function (list, str) {
        console.log("\n[*]com.netease.cloudmusic.b.a.a begin.");
        console.log("[*] list -> " + list);
        console.log("[*] str -> " + str);

        var res = this.b(list, str);
        console.log("[*] res -> " + res);
        return res
    }

    var base64DecodeClass = Java.use("a.auu.a");
    base64DecodeClass.c.implementation = function (str) {
        var res = this.c(str);
        if (str.indexOf("JgEOXBgeEDcBChZX") != -1) {
            console.log("\n[*] Base64 decode begin.");
            console.log("[*] a.auu.a.c(" + str + ") -> " + res);
        }
        return res;
    }

    var strClass = Java.use("java.lang.String");
    console.log("[*] Base64 decode JgEOXBgeEDcBChZX -> " + base64DecodeClass.$new().c(strClass.$new("JgEOXBgeEDcBChZX")));
    console.log("[*] Base64 decode NQUEAQ== -> " + base64DecodeClass.$new().c(strClass.$new("NQUEAQ==")));
    console.log("[*] Base64 decode KBsQGxoD -> " + base64DecodeClass.$new().c(strClass.$new("KBsQGxoD")));
    console.log("[*] Base64 decode KAEBGxUVGiQDBg== -> " + base64DecodeClass.$new().c(strClass.$new("KAEBGxUVGiQDBg==")));
    console.log("[*] Base64 decode KA8NBx8RFzEbERcL -> " + base64DecodeClass.$new().c(strClass.$new("KA8NBx8RFzEbERcL")));
    console.log("[*] Base64 decode JxwCHB0= -> " + base64DecodeClass.$new().c(strClass.$new("JxwCHB0=")));
    console.log("[*] Base64 decode NhoCAA0FBGoeCBUK -> " + base64DecodeClass.$new().c(strClass.$new("NhoCAA0FBGoeCBUK")));
    console.log("[*] Base64 decode NgsRBBwCVDcLEAcVBFQgAxMGAA== -> " + base64DecodeClass.$new().c(strClass.$new("NgsRBBwCVDcLEAcVBFQgAxMGAA==")));
});