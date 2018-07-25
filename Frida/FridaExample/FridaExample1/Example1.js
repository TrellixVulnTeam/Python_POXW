console.log("Script loaded successfully!");
Java.perform(function () {
    console.log("Inside java perform function.");
    var my_class = Java.use("com.example.a11x256.frida_test.my_activity");
    my_class.fun.implementation = function (x, y) {
        console.log("Original call:fun(" + x + "," + y + ")");
        var ret_value = this.fun(2,5);
        return ret_value;
    }
});