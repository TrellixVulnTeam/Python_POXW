Java.perform(function () {
    console.log("Begin Javascript.");

    // 1、提取基本信息
    var oriData = Java.use("com.wifi.connect.plugin.magickey.d.c");
    oriData.a.overload('java.lang.String', 'com.lantern.core.model.WkAccessPoint', 'java.util.ArrayList', 'java.lang.String', 'java.lang.String').implementation = function (arg1, arg2, arg3, arg4, arg5) {
        console.log("[*] 提取基本信息");
        var ret = this.a(arg1, arg2, arg3, arg4, arg5);
        console.log("[*] arg1 -> " + arg1);
        console.log("[*] arg2 -> " + arg2);
        console.log("[*] arg3 -> " + arg3);
        console.log("[*] arg4 -> " + arg4);
        console.log("[*] arg5 -> " + arg5 + "\n");
        console.log("[*] ret ->" + ret);
        send(ret);
        console.log("\n");
        return ret;
    };

    // 2、产生request的输入body
    var bluefayFunc = Java.use("com.lantern.core.x");
    bluefayFunc.a.overload('java.lang.String', '[B').implementation = function (arg1, arg2) {
        var ret = this.a(arg1, arg2);

        if (arg1 === "00302002") {
            console.log("[*] 产生request的输入body");
            console.log("[*] arg1 -> " + arg1);
            console.log("[*] arg2 -> ");
            send(arg2);
            console.log("\n");
            console.log("[*] com.lantern.core.x.a -> ");
            send(ret);
            console.log("\n");
        }

        return ret;
    };

    // 3、密码获取response
    var stackFunc = Java.use("com.wifi.connect.plugin.magickey.e.d");
    stackFunc.a.overload('java.lang.String', '[B').implementation = function (arg1, arg2) {
        var ret = this.a(arg1, arg2);

        console.log("[*] 密码获取response");
        console.log("[*] arg1 is -> " + arg1);
        console.log("[*] arg2 is -> ");
        send(arg2);
        console.log("\n");
        console.log("[*] com.wifi.connect.plugin.magickey.e.da(arg) -> ");
        send(ret);
        console.log("\n");
        return ret;
    };

    // 4、密码解密
    var pwdDecodeCls = Java.use("com.lantern.core.WkSecretKeyNative");
    pwdDecodeCls.a.overload('java.lang.String', 'java.lang.String').implementation = function (str, str2) {
        var ret = this.a(str, str2);

        console.log("[*] 密码解密");
        console.log("[*] str -> " + str);
        console.log("[*] str2 -> " + str2 + "\n");
        console.log("[*] ret -> " + ret);
        console.log("\n");
        return ret;
    };

    // resquest解析

    // var Exc = Java.use("java.lang.Exception");
    // var Log = Java.use("android.util.Log");
    // var stackFunc = Java.use("com.wifi.connect.plugin.magickey.e.d");
    // stackFunc.a.overload('java.lang.String', '[B').implementation = function (arg1, arg2) {
    //     var e = Exc.$new("");
    //     var log = Log.$new();
    //     console.log(log.getStackTraceString(e));
    //     return this.a(arg1, arg2);
    // };

    // var bluefayFunc = Java.use("com.bluefay.b.d");
    // bluefayFunc.a.overload('[B').implementation = function (bArg) {
    //     console.log("[*] Script Begin! ");
    //     var ret = this.a(bArg)
    //     var result = send(ret);
    //     console.log("[*] com.bluefay.b.d.a(arg) arg is -> " + result + "\n");
    //
    //     return ret;
    // };

    // com.lantern.core.x类 函数
    // var coreXA = Java.use("com.lantern.core.x");
    // coreXA.a.overload('boolean', 'java.lang.String').implementation = function (z, str) {
    //     var ret = this.a(z, str);
    //
    //     if (str === "k") {
    //         console.log("[*] com.lantern.core.x(z, str) Begin!");
    //         console.log("[*] z -> " + z);
    //         console.log("[*] str -> " + str);
    //         console.log("[*] ret -> ");
    //         send(ret);
    //         console.log("\n")
    //     }
    //     return ret;
    // };

    // coreXA.a.overload('[B', 'java.lang.String', 'boolean', 'boolean').implementation = function (bArr, str, z, z2) {
    //     var ret = this.a(bArr, str, z, z2);
    //
    //     if (z && z2 && str === "k") {
    //         console.log("[*] com.lantern.core.x(bArr, str, z, z2) Begin!");
    //         console.log("[*] bArr -> ");
    //         send(bArr);
    //         console.log("[*] str -> " + str);
    //         console.log("[*] ret -> ");
    //         send(ret);
    //         console.log("\n");
    //     }
    //
    //     return ret;
    // };

    // com.lantern.core.e类，始终返回A，地址为 http://ap.51y5.net/ap/fa.sec
    // var coreEA = Java.use("com.lantern.core.e");
    // coreEA.a.overload().implementation = function () {
    //     return "A";
    // }

    // var conventCls = Java.use("com.lantern.core.p.b");
    // conventCls.a.overload('boolean', 'boolean', 'java.lang.String', 'java.lang.String', '[B').implementation = function (z, z2, str, str2, bArr) {
    //     var ret = this.a(z, z2, str, str2, bArr);
    //
    //     if (str2 === "00302002") {
    //         console.log("[*] com.lantern.core.p.b.a(z, z2, str, str2, bArr) Begin!");
    //         console.log("[*] z -> " + z);
    //         console.log("[*] z2 -> " + z2);
    //         console.log("[*] str -> " + str);
    //         console.log("[*] str2 -> " + str2);
    //         console.log("[*] bArr -> ");
    //         send(bArr);
    //         console.log("[*] ret -> ");
    //         send(ret);
    //         console.log("\n")
    //     }
    //     return ret;
    // };

    // response解析

    // var responseCls = Java.use("com.lantern.core.x");
    // responseCls.b.overload('[B', 'java.lang.String', 'boolean', 'boolean').implementation = function (bArr, str, z, z2) {
    //     var ret = this.b(bArr, str, z, z2);
    //
    //     console.log("[*] bArr -> ");
    //     send(bArr);
    //     console.log("[*] str -> " + str);
    //     console.log("[*] z -> " + z);
    //     console.log("[*] z2 -> " + z2);
    //     console.log("[*] ret -> ");
    //     send(ret);
    //     console.log("\n");
    //
    //     return ret;
    // };

    // responseCls.b.overload('java.lang.String', '[B').implementation = function (str, bArr) {
    //     var ret = this.b(str, bArr);
    //
    //     console.log("[*] str -> " + str);
    //     console.log("[*] bArr -> ");
    //     send(bArr);
    //     console.log("[*] ret -> ");
    //     send(ret.g());
    //     console.log("\n");
    //
    //     return ret;
    // };

    // var pwdCls = Java.use("com.wifi.connect.plugin.magickey.d.c");
    // pwdCls.a.overload('[B', 'java.lang.String').implementation = function (bArr, str) {
    //     var ret = this.a(bArr, str);
    //
    //     // [*] bArr ->
    //     // b'\x00\x00\x00\x00\x00kT\xf1\xd7\x10\\\xb6\xd5_X\x98\x0bR\xcb\xc5\x01p\xe3\x85Ul\xf5W\x9d5\x17\xba\n8\xeag\xd4C,\t\xdeO\x9a\xa4O\xdb\x1f"q{\xc5}\xf5\xb9\xb9&P,p5\x020\x8b \xbf\x07\xaeI]/y\xa87U\x82\xe0\xf73\xd4\xf9\xaf\xd1\xc7\xdfHj\xd3\xc6\x9e\x02\x85u^*\x81\xab\x9e\xae\xd3\xfe\xbaL\x08\x98\x94(\x01\x93\xfdQj\x00M\xb2\xcd\x95c1\xb2\x11\xe9,\x98\x85\x0e\xce\x8d\xc0T\xb2\x8d\xf8\x06\x94\xfd\xb5\n\x9e\xd8\xff\xa7\xc6\x15\x16\x94%{Th\x92b7\xe3\xd9\xa7W\x0c ?1\x9c}\x12Db\xb9\x0e#Rx!(\x1f\xf1\xf5o\x1a.j4"/:\\\x17\xfbI\xe4\xb1:\x84/\xb6\t\xf8d\x96\xd6\xa1\xd8W\xbc\x80\xaasgr\xd6\x0f\xe5\xc7\x9c Sy8p\xafM\x11\xd3\x84\xc9L5\xe8\xb4p\x8b\x18\xae\xa9\xf9\xe9V<B\xfbe\x01i\xbag\xe5\xc8\xae:\xa0\x06y\x14\x90\xf6\x8c\x12\xf9[\x92\xa6\x92\xd0\xfd"\x0bN)L\x90\x99\xf4'
    //     // [*] str -> 00302002
    //     // [*] ret -> {"retcode":"0","retmsg":"","qid":"c0a8dd4246a25bb06e2605770574","sysTime":1538289190798,"s":false,"aps":["pwdid:af601d7d3566494b8b3d2e83673ec0fb\npwd:apple7899\napid:7112D2AE3D5E4E261A2AEB16D380152B\nccId:null\nkeystatus:0\nauthType:0\nsecurity:0"]}
    //
    //     console.log("[*] com.wifi.connect.plugin.magickey.d.c(bArr, str) begin.");
    //     console.log("[*] bArr -> ");
    //     send(bArr);
    //     console.log("[*] str -> " + str);
    //     console.log("[*] ret -> " + ret);
    //     console.log("\n");
    //     return ret;
    // };

    // var AesKeyCls = Java.use("com.lantern.core.n.l");
    // AesKeyCls.a.overload('java.lang.String').implementation = function (str) {
    //     var ret = this.a(str);
    //
    //     console.log("[*] com.lantern.core.n.l.a(str) begin.");
    //     console.log("[*] str -> " + str);
    //     console.log("[*] ret -> " + ret);
    //     console.log("\n");
    //     return ret;
    // };

    // Native层注入
    // Module.enumerateExports("libwkcore.so", {            // 枚举模块中包含的符号。enumerateSymbolsSync(name)为同步版本，返回符号的列表
    //     onMatch: function (sym) {
    //         console.log("\n[*] sym.isGlobal -> " + sym.isGlobal);   //bool类型，表示符号是否全局可见
    //         console.log("[*] sym.type -> " + sym.type);   //符号的类型，包括unknown,section,undefined (Mach-O),absolute (Mach-O),prebound-undefined (Mach-O),indirect (Mach-O),object (ELF),function (ELF),file (ELF),common (ELF),tls (ELF)。
    //         if (sym.section) {          // 节区信息。不一定含有
    //             console.log("[*] sym.section.id -> " + sym.section.id);   // 节区名称
    //             console.log("[*] sym.section.protection -> " + sym.section.protection);   // 节区保护属性，r-x、rwx等
    //         }
    //         console.log("[*] sym.name -> " + sym.name);   // 符号名称
    //         console.log("[*] sym.address -> " + sym.address);   // 符号的绝对地址
    //     },
    //     onComplete: function () {
    //         console.log("[*] onComplete! ");
    //     }
    // });


    // Interceptor.attach(Module.findExportByName("libwifi_core.so", "Java_com_lantern_core_WkSecretKeyNative_dp"), {       // Interceptor拦截器附着(attach)所有函数名为dlopen
    //     onEnter: function (args) {                              // 拦截函数进入时的操作
    //         console.log("[*] Interceptor.attach.onEnter!");
    //         for (var arg in args) {
    //             console.log("[*] args[" + arg + "] -> " + args[arg])
    //         }
    //         console.log('[*] Context information:');
    //         console.log('[*] Context  : ' + JSON.stringify(this.context));
    //         console.log('[*] Return   : ' + this.returnAddress);
    //         console.log('[*] ThreadId : ' + this.threadId);
    //         console.log('[*] Depth    : ' + this.depth);
    //         console.log('[*] Errornr  : ' + this.err);
    //     },
    //     onLeave: function (retval) {                            // 函数返回后的操作
    //         console.log("[*] Interceptor.attach.onLeave!");
    //         for (var r in retval) {
    //             console.log("[*] retval[" + r + "] -> " + retval[r])
    //         }
    //     }
    // });

    // 动态库载入分析
    // var WkSecretKeyNativeNew = Java.use(" com.lantern.core.WkSecretKeyNativeNew");
    // WkSecretKeyNativeNew.tryLoadLibrary.implementation = function (str, str2, context) {
    //     console.log("[*] str -> " + str);
    //     console.log("[*] str2 -> " + str2);
    //     console.log("[*] context.getFilesDir() -> " + context.getFilesDir());
    //
    //     return this.tryLoadLibrary(str, str2, context);
    // }
});