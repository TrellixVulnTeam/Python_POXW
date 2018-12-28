console.log("[*] Starting script");

////-------------------------console接口------------------------
// var libc = Module.findBaseAddress("libc.so");
// var buf = Memory.readByteArray(libc, 256);
// console.log(hexdump(buf, {
//     offset: 0,
//     length: 256,
//     header: true,
//     ansi: false
// }));

////-----------------------------Frida接口----------------------------------------
// console.log("[*] Frida.version  -> " + Frida.version);
// console.log("[*] Frida.heapSize -> " + Frida.heapSize);

////-----------------------------Process接口-----------------------------------------
// console.log("\n[*] Process.arch -> " + Process.arch);       // 打印cpu的平台，ia32, x64, arm or arm64
// console.log("[*] Process.platform -> " + Process.platform);     // 打印目标操作系统，linux、windows
// console.log("[*] Process.pageSize -> " + Process.pageSize);         // 打印虚拟页面大小
// console.log("[*] Process.pointerSize -> " + Process.pointerSize);   // 打印指针占用的内存大小
// console.log("[*] Process.codeSigningPolicy -> " + Process.codeSigningPolicy);     // 默认值是 optional，除非是在 Gadget 模式下通过配置文件来使用 required，通过这个属性可以确定 Interceptor API 是否有限制，确定代码修改或者执行未签名代码是否安全。
// console.log("[*] Process.isDebuggerAttached() -> " + Process.isDebuggerAttached());     // 确定当前是否有调试器附加
// console.log("[*] Process.getCurrentThreadId() -> " + Process.getCurrentThreadId());     // 获取当前线程ID
//
// Process.enumerateThreads({                  // 枚举所有线程
//     onMatch: function (thread) {
//         console.log("\n[*] thread.id -> " + thread.id);     // 打印线程id
//         console.log("[*] thread.state -> " + thread.state);     // 打印线程状态
//         console.log("[*] thread.context -> " + thread.context);     // 打印寄存器
//     },
//     onComplete: function () {
//     }
// });
//
// var thread_list = Process.enumerateThreadsSync();        // 枚举线程同步版本，返回线程列表
// for (var index in thread_list) {
//     console.log("[*] thread_list[index].id -> " + thread_list[index].id);     // 打印线程id
//     console.log("[*] thread_list[index].state -> " + thread_list[index].state);     // 打印线程状态
//     console.log("[*] thread_list[index].context -> " + thread_list[index].context);     // 打印寄存器
// }
//
// Process.enumerateModules({                  // 枚举所有模块
//     onMatch: function (module) {
//         console.log("\n[*] module.name -> " + module.name);     //打印模块名字
//         console.log("[*] module.base -> " + module.base);     // 打印模块基地址
//         console.log("[*] module.size -> " + module.size);     // 打印模块大小
//         console.log("[*] module.path -> " + module.path);     // 打印模块路径
//     },
//     onComplete: function () {
//     }
// });
//
// var module_list = Process.enumerateModulesSync();       // 枚举所有的模块同步版本。返回模块列表
// for (var index in module_list) {
//     console.log("\n[*] module_list[index].name -> " + module_list[index].name);     //打印模块名字
//     console.log("[*] module_list[index].base -> " + module_list[index].base);     // 打印模块基地址
//     console.log("[*] module_list[index].size -> " + module_list[index].size);     // 打印模块大小
//     console.log("[*] module_list[index].path -> " + module_list[index].path);     // 打印模块路径
// }
//
// var libc_module = Process.getModuleByName("libc.so");       // 根据模块的名字查找模块
// libc_module = Process.findModuleByAddress(libc_module.base);        // 根据模块的地址查找模块
// console.log("\n[*] Process.findModuleByName(\"libc.so\"):");
// console.log("[*] libc_module.name -> " + libc_module.name);     //打印模块名字
// console.log("[*] libc_module.base -> " + libc_module.base);     // 打印模块基地址
// console.log("[*] libc_module.size -> " + libc_module.size);     // 打印模块大小
// console.log("[*] libc_module.path -> " + libc_module.path);     // 打印模块路径
//
// var cache_block = Process.findRangeByAddress(Process.getModuleByName("libc.so").base);  // 获取目标内存块信息，地址找不到返回null。getRangeByAddress则会抛出异常
// console.log("\n[*] cache_block.base -> " + cache_block.base);     // 内存块的基地址
// console.log("[*] cache_block.size -> " + cache_block.size);     // 内存块大小
// console.log("[*] cache_block.protection -> " + cache_block.protection); // 内存块保护属性，r-x、rwx等
// console.log("[*] cache_block.file.path -> " + cache_block.file.path);   // 内存块对应文件路径
// console.log("[*] cache_block.file.offset -> " + cache_block.file.offset);   // 内存块对应文件内偏移
// console.log("[*] cache_block.file.size -> " + cache_block.file.size);   // 内存块对应文件大小
//
// Process.enumerateRanges("r-x", {        // 枚举指定 protection 类型的内存块
//     onMatch: function (range) {         // 匹配到指定内存块的操作
//         console.log("\n[*] range.base -> " + range.base);     // 内存块的基地址
//         console.log("[*] range.size -> " + range.size);     // 内存块大小
//         console.log("[*] range.protection -> " + range.protection); // 内存块保护属性，r-x、rwx等
//         if (range.file) {           // 如果含有file属性的话，打印file属性的内部参数
//             console.log("[*] range.file.path -> " + range.file.path);   // 内存块对应文件路径
//             console.log("[*] range.file.offset -> " + range.file.offset);   // 内存块对应文件内偏移
//             console.log("[*] range.file.size -> " + range.file.size);   // 内存块对应文件大小
//         }
//     },
//     onComplete: function () {
//         console.log("[*] onComplete! ");
//     }
// });

////-----------------------------------Module接口--------------------------------------------
// Module.enumerateImports("libwechatnormsg.so", {      // 根据模块的名称，枚举指定模块从其他模块中导入的项。enumerateImportsSync(name)同步版本，返回导入项列表
//     onMatch: function (imp) {
//         console.log("\n[*] imp.type -> " + imp.type);       // 导入项的类型，function 或者 variable
//         console.log("[*] imp.name -> " + imp.name);         // 导入项的名称
//         console.log("[*] imp.module -> " + imp.module);     // 与导入项关联的模块的名称
//         console.log("[*] imp.address -> " + imp.address);   // 导入项的绝对地址
//     },
//     onComplete: function () {
//         console.log("[*] onComplete! ");
//     }
// });
//
// Module.enumerateExports("libwechatnormsg.so", {      // 根据模块的名称，枚举指定模块被其他模块使用的导出的项。enumerateExportsSync(name)同步版本，返回导出项列表
//     onMatch: function (exp) {
//         console.log("\n[*] exp.type -> " + exp.type);       // 导出项的类型
//         console.log("[*] exp.name -> " + exp.name);         // 导出项的名称
//         console.log("[*] exp.address -> " + exp.address);   // 导出项的绝对地址
//     },
//     onComplete: function () {
//         console.log("[*] onComplete! ");
//     }
// });
//
// Module.enumerateSymbols("libc.so", {            // 枚举模块中包含的符号。enumerateSymbolsSync(name)为同步版本，返回符号的列表
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

////---------------------------------------------Memory属性-----------------------------------------------
// 在 address 开始的地址，size 大小的内存范围内以 pattern 这个模式进行匹配查找，查找到一个内存块就回调callbacks
// Memory.scan(Module.findBaseAddress("libc.so"), 1024, "50 e5 ?? 64", {       // Memory.scanSync为同步版本，但会匹配信息的列表
//     onMatch: function (address, size) {                     // 根据条件匹配到相应的内存块后，回调匹配信息
//         console.log("[*] Memory.scan.onMatch.address -> " + address);   // 打印匹配到的地址
//         console.log("[*] Memory.scan.onMatch.size -> " + size);     // 打印匹配到的内容长度
//     },
//     onError: function (reason) {            // 异常处理
//         console.log("[*] Memory.scan.onError.reason -> " + reason);
//     },
//     onComplete: function () {
//         console.log("[*] Memory.scan.onComplete over.");
//     }
// });
//
// var buf = Memory.alloc(128);       // 在目标进程的堆上分配size字节的空间
// console.log("\n[*] Before copy: ");
// console.log(hexdump(buf, {          // 打印buf的内容
//     offset: 0,
//     length: 128,
//     header: true,
//     ansi: false                 // ansi为windows系统下的字体
// }));
//
// Memory.copy(buf, Module.findBaseAddress("libc.so"), 128);         // 从src地址拷贝规定size的内容至dst地址
// console.log("\n[*] After Memory.copy -> " );
// console.log(hexdump(buf, {
//     offset: 0,
//     length: 128,
//     header: true,
//     ansi: false
// }));
//
// console.log("\n[*] After Memory.dup -> " );
// var buf2 = Memory.dup( Module.findBaseAddress("libc.so"), 64);      // dup结合了alloc和copy的操作，从指定地址开始，复制大小为size的内容，返回复制后的内容
// console.log(hexdump(buf2, {
//     offset: 0,
//     length: 128,
//     header: true,
//     ansi: false
// }));
//
var cache_block = Process.findRangeByAddress(Process.getModuleByName("libc.so").base);  // 获取原始libc.so模块内存信息
console.log("\n[*] Before Memory.protect:");
console.log("[*] JSON.stringify() -> " + JSON.stringify(cache_block));
console.log("[*] cache_block.base -> " + cache_block.base);     // 原始内存块的基地址
console.log("[*] cache_block.size -> " + cache_block.size);     // 原始内存块的大小
console.log("[*] cache_block.protection -> " + cache_block.protection); // 原始内存块的保护属性为r-x
//
// Memory.protect(cache_block.base, cache_block.size, "rwx");      // 修改内存块的保护属性为rwx
// var cache_block2 = Process.findRangeByAddress(Process.getModuleByName("libc.so").base); // 重新读取libc.so模块内存信息
// console.log("\n[*] After Memory.protect:");
// console.log("[*] cache_block2.base -> " + cache_block2.base);     // 修改后内存块的基地址  不变
// console.log("[*] cache_block2.size -> " + cache_block2.size);     // 修改后内存块大小  不变
// console.log("[*] cache_block2.protection -> " + cache_block2.protection); // 修改后内存块的保护属性  改变为rwx
//
// var pointerValue = Memory.readPointer(Process.getModuleByName("libc.so").base);     // 读取指定地址处的值
// console.log("[*] Before Memory.writePointer-> " + pointerValue);
//
// Memory.writePointer(libc_address, ptr("0x78563412"));       // 在指定内存地址处写入值
// pointerValue = Memory.readPointer(Process.getModuleByName("libc.so").base);
// console.log("[*] After Memory.writePointer -> " + pointerValue);
//
//
// Memory.writeByteArray(Process.getModuleByName("libc.so").base, [0xff, 0xff]);           // 在指定地址，写入对应的字节数组
// var valueArr = Memory.readByteArray(Process.getModuleByName("libc.so").base, 128);      // 读取指定地址，规定size大小的内容。读取的内容需要通过hexdump接口展示
// console.log("[*] Memory.readByteArray -> " + valueArr);
// console.log(hexdump(valueArr, {
//     offset: 0,
//     length: 128,
//     header: true,
//     ansi: false
// }));

////---------------------------------------------Frida基础类型-----------------------------------------------
// var int_v = new Int64(64);
// console.log("\n[*] new Int64(64) -> " + int_v);       // Int64(v)、UInt64(v) 需要使用关键字new来创建
// console.log("[*] int64(64) -> " + int64(64));   // int64(v)、uint64(v) 不需要，可直接创建
// console.log("[*] int_v.toString(radix = 16) -> 0x" + int_v.toString(radix = 16));     // 按照对应进制进行转换（貌似只有十进制和十六进制选择）
//
// var nativePointerA = new NativePointer("0x123456");
// console.log("\n[*] new NativePointer(\"0x123456\") -> " + nativePointerA);      // 指针类型变量
// console.log("[*] ptr(\"0x123456\") -> " + ptr("0x123456"));
// console.log("[*] ptr(\"0x123456\") + ptr(\"0x111111\") -> " +  ptr("0x123456").add(0x111111));    // 指针类型变量不能直接相加，需要使用add()接口
// console.log("[*] nativePointerA.toInt32() -> " + nativePointerA.toInt32());         // 转换成int类型
// console.log("[*] nativePointerA.toString() -> " + nativePointerA.toString(radix=10));       // 按进制转换成对应进制的值
//
// var nativeFunctionA = new NativeFunction(Module.findExportByName("libc.so", "getpid"), "void", ["void"]);
// console.log("\n[*] new NativeFunction(Module.findExportByName(\"libc.so\", \"getpid\"), \"void\", [\"void\"]) -> " + nativeFunctionA);

////---------------------------------------------Interceptor接口----------------------------------------------
// Interceptor.attach(Module.findExportByName("libc.so", "open"), {       // Interceptor拦截器附着(attach)所有函数名为dlopen
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

////---------------------------------------------Java接口----------------------------------------------
// console.log("\n[*] Java.available -> " + Java.available);       // 判断Java环境是否可用
// Java.perform(function () {                  // 执行任意 Java 操作都需要使⽤此函数
    // Java.enumerateLoadedClasses({                // 枚举加载的类。enumerateLoadedClassesSync() 为同步版本，返回值为类名的列表。
    //     onMatch: function (className) {          // 匹配到时，参数为类名
    //         console.log("\n[*] className -> " + className);
    //     },
    //     onComplete: function () {
    //         console.log("[*] Java.enumerateLoadedClasses.onComplete -> ");
    //     }
    // });
    //
    // var logClass = Java.use("com.tencent.mm.sdk.platformtools.x");  // 获取指定类名的JavaScript引用
    // logClass.i.overload("java.lang.String", "java.lang.String").implementation = function (arg1, arg2) {    // 源代码中含有重载的函数接口，这里要指定。
    //     if ("MicroMsg.LauncherUI" === arg1) {
    //         console.log("\n[*] logClass.i.overload(\"java.lang.String\", \"java.lang.String\")");
    //         console.log("[*] Original arg1 -> " + arg1);
    //         console.log("[*] Original arg2 -> " + arg2);
    //     }
    //     this.i(arg1, arg2);     // 如果不运行源函数功能，则源函数也不会运行
    // };
    //
    // var strClass = Java.use("java.lang.String");
    // logClass.i.overload("java.lang.String", "java.lang.String", '[Ljava.lang.Object;').implementation = function (arg1, arg2, arg3) {
    //     if ("MicroMsg.LauncherUI" === arg1) {
    //         // 使用JavaScript引用类的功能，包括：
    //         // $new：new 运算符，初始化新对象。注意与 $init 区分
    //         // $alloc：分配内存，但不不初始化
    //         // $init：构造器器⽅方法，⽤用来 hook ⽽而不不是给 js 调⽤用，可以用来返回类实例化对象，return this.$init(args...)
    //         // $dispose：析构函数
    //         // $isSameObject：是否与另⼀一个 Java 对象相同
    //         // $className：类名
    //         console.log("\n[*] strClass.$className -> " + strClass.$className);
    //         console.log("[*] strClass.$new(\"Hello World!) -> " + strClass.$new("Hello World!"));
    //     }
    //     return this.i(arg1, arg2, arg3);
    // };
    //
    // var bool_a = Java.use("java.lang.Boolean").$new(true);      // 与Java相关的接口，必须在Java.perform(function(){...}) 规定的函数外层使用，内层不能使用。
    // Java.scheduleOnMainThread(function () {
    //     // var bool_a = Java.use("java.lang.Boolean").$new(true);       // 错误的做法
    //     console.log("[*] Java.use(\"java.lang.Boolean\").$new(true) -> " + bool_a);
    // });

    // Java.choose("com.tencent.mm.ui.LauncherUI", {     // 在Java的内存堆上扫描指定类名称的Java对象，每次扫描到一个对象，则回调callbacks
    //     onMatch: function (instance) {              // 参数为目标的单例
    //         for (var i in instance) {
    //             console.log("[*] instance[" + i + "] -> " + instance[i]);
    //         }
    //     },
    //     onComplete: function () {
    //         console.log("[*] Java.choose().onComplete!")
    //     }
    // });
    //
    // Java.cast(ptr("0x1234"), Java.use("java.lang.String"));     // 将指定地址的内容强转为目标类型(使用Java.use()后的对象)
// });

console.log("[*] Stoping script");