Java.perform(function () {
    var logClass = Java.use("com.tencent.mm.sdk.platformtools.x");
    logClass.i.overload("java.lang.String", "java.lang.String").implementation = function (str1, str2) {
       console.log("*************************************");
       console.log("Original arg: " + str1);
        // for (var id in str1){
        //     console("[*]str1: " + id);
        // }
        // // console("[*]str1: " + str1.type);
        // // console("[*]str2: " + str2);
        // this.i(str1, str2);
    };
});
