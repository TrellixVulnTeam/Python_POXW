Java.perform(function () {
    // var intentClass = Java.use("com.tencent.mm.plugin.emoji.ui.CustomSmileyPreviewUI");
    // intentClass.n.implementation = function (customSmileyPreviewUI) {
    //         console.log("*************************************");
    //         console.log("Retr_File_Name: " + customSmileyPreviewUI.getIntent().getStringExtra("custom_smiley_preview_md5"));
    //         console.log("Retr_Msg_Id: " + customSmileyPreviewUI.getIntent().getIntExtra("CropImage_Msg_Id", -1));
    //         console.log("Retr_Compress_Type: " + customSmileyPreviewUI.getIntent().getIntExtra("CropImage_CompressType", 0));
    //         console.log("\n");
    //         return this.n(customSmileyPreviewUI);
    // }

    // var logClass = Java.use("com.tencent.mm.sdk.platformtools.x");
    // logClass.i.overload("java.lang.String", "java.lang.String").implementation = function (str1, str2) {
    //     if ("MicroMsg.LauncherUI" === str1) {
    //         console.log("*************************************");
    //         console.log("Original arg1: " + str1);
    //         console.log("Original arg2: " + str2);
    //         console.log("\n");
    //     }
    //     this.i(str1, str2);
    // };

    // logClass.i.overload("java.lang.String", "java.lang.String", '[Ljava.lang.Object').implementation = function (str1, str2, str3) {
    //     if ("MicroMsg.LauncherUI" === str1) {
    //         console.log("*************************************");
    //         console.log("Original arg1: " + str1);
    //         console.log("Original arg2: " + str2);
    //         console.log("Original arg3: " + str3);
    //         console.log("\n");
    //     }
    //     return this.i(str1, str2, str3);
    // };

    // var logClass = Java.use("com.tencent.mm.sdk.platformtools.x");
    // logClass.d.overload("java.lang.String", "java.lang.String", "[Ljava.lang.Object;").implementation = function (str1, str2, strArr) {
    //     // if ("MicroMsg.RsaInfo" === str1) {
    //         console.log("*************************************");
    //         console.log("Original arg1: " + str1);
    //         console.log("Original arg2: " + str2);
    //         console.log("Original arg3: " + strArr);
    //         console.log("\n");
    //     // }
    //     this.d(str1, str2, strArr);
    // };

    var TbsLogClass = Java.use("com.tencent.smtt.utils.TbsLog");
    TbsLogClass.i.overload("java.lang.String", "java.lang.String", "boolean").implementation = function (str1, str2, strArr) {
        // if ("MicroMsg.RsaInfo" === str1) {
            console.log("**************（str, str, bool）***********************");
            console.log("Original arg1: " + str1);
            console.log("Original arg2: " + str2);
            console.log("Original arg3: " + strArr);
            console.log("\n");
        // }
        this.i(str1, str2, strArr);
    };

    TbsLogClass.i.overload("java.lang.String", "java.lang.String").implementation = function (str1, str2) {
        // if ("MicroMsg.RsaInfo" === str1) {
            console.log("***************(str, str)**********************");
            console.log("Original arg1: " + str1);
            console.log("Original arg2: " + str2);
            console.log("\n");
        // }
        this.i(str1, str2);
    };
});
