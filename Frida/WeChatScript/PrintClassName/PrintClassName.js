Java.perform(function () {
    Java.enumerateLoadedClasses({
        onMatch: function (className) {
            send("{ \"classname\": \"" + className + "\"}");
        },
        onComplete: function () {
        }
    });
});

