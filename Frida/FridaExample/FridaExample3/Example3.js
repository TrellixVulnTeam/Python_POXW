console.log("Script loaded successfully!");
var instances_array = [];
function callSecretFun() {
    Java.perform(function () {
        if (instances_array.length === 0){
            Java.choose("com.example.a11x256.frida_test.my_activity", {
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    instances_array.push(instance);
                    console.log("if, secret result is: " + instance.secret());
                },
                onComplete: function () {}
            })
        }
        else {
            for (i = 0; i < instances_array.length; i++){
                console.log("else, secret result is: " + instances_array[i].secret())
            }
        }
    })
}


rpc.exports = {
    callsecretfunction: callSecretFun
};