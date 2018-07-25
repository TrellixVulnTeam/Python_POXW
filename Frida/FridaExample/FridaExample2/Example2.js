// console.log("Script loaded successfully!");
// Java.perform(function () {
//     console.log("Inside java perform function.");
//     var my_class = Java.use("com.example.a11x256.frida_test.my_activity");
//     my_class.fun.implementation = function (x, y) {
//         console.log("Original call:fun(" + x + "," + y + ")");
//         var ret_value = this.fun(2,5);
//         return ret_value;
//     }
// });

console.log("Script loaded successfully!");
Java.perform(function () {
    console.log("Inside java perform function.");
    var my_class = Java.use("com.example.a11x256.frida_test.my_activity");
    my_class.fun.overload("int", "int").implementation = function (x, y) {
        // hook func(x,y)
        console.log("*************func(x, y)**************");
        console.log("Original call:fun(" + x + "," + y + ")");
        var ret_value = this.fun(2, 5);
        console.log("*************************************\n");
        return ret_value;
    };

    // 对指定类名动态的获取这个类的JavaScript引用，后续可以使用$new()来调用类的构造函数进行类对象的创建。
    var string_class = Java.use("java.lang.String");
    my_class.fun.overload("java.lang.String").implementation = function (x) {
        // hook func(string)
        console.log("*************func(string)**************");
        var my_string = string_class.$new("This is Testing####");
        console.log("Original call: func(" + x + ")");
        var ret = this.fun(my_string);
        console.log("this.fun(my_string) return value is:" + ret);
        this.total.value = "123";           // 通过value给类中的变量赋值
        console.log("secret return: " + this.secret());
        console.log("****************************************\n");
        return ret;
    };

    // my_class.total = string_class.$new(" hello world");
    // my_class.secret.implementation = function () {
    //     console.log("*************secret()**************");
    //     var ret = this.secret();
    //     return ret;
    // };

    // 在Java的内存堆上扫描指定类名称的Java对象，没次扫描到一个对象，则回调callbacks。
    Java.choose("com.example.a11x256.frida_test.my_activity", {
        onMatch: function (instance) {
            // console.log("Found instance: " + instance);
            // send("Found instance: " + instance);

            // instance.total.value = string_class.$new(" hello world");
            console.log("instance.total = " + instance.total.value);
            console.log("Result of secret func: " + instance.secret());
        },
        onComplete: function () {
            console.log("call onComplete: function ()");
        }
    });
});