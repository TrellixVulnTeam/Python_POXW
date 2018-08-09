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

    function PrintValue(name, argValue) {
        console.log("[*] " + name + ":");
        for (var i in argValue) {
            console.log("   " + name + "[" + i + "] -> " + argValue[i]);
        }
        console.log("\n");
    }

    function PrintBytes(arg) {
        var memory_regions = new Array();
        for (var i = 0; i < arg.length; i++) {
            memory_regions.push(arg[i]);
        }

        var str = "";
        for (var i = 0; i < memory_regions.length; i++) {
            str += (memory_regions[i].toString(16) + " ");
        }
        console.log(arg + " -> " + str);
    }

    var unpackClass = Java.use("com.tencent.mm.protocal.MMProtocalJni");
    unpackClass.unpack.implementation = function (arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8) {
        console.log("\n[*] com.tencent.mm.protocal.MMProtocalJni.unpack :");
        PrintBytes(arg1);
        PrintBytes(arg2);
        PrintBytes(arg3);
        PrintBytes(arg4);
        PrintBytes(arg5);
        PrintBytes(arg6);
        PrintBytes(arg7);
        PrintBytes(arg8);
        return this.unpack(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8);
    };

    var packClass = Java.use("com.tencent.mm.protocal.MMProtocalJni");
    packClass.pack.implementation = function (arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12) {
        console.log("\n[*] com.tencent.mm.protocal.MMProtocalJni.pack :");
        PrintValue(arg1, arg1);
        PrintValue(arg2, arg2);
        PrintValue(arg3, arg3);
        PrintValue(arg4, arg4);
        PrintValue(arg5, arg5);
        PrintValue(arg6, arg6);
        PrintValue(arg7, arg7);
        PrintValue(arg8, arg8);
        PrintValue(arg9, arg9);
        PrintValue(arg10, arg10);
        PrintValue(arg11, arg11);
        PrintValue(arg12, arg12);
        return this.pack(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12);
    }
});
