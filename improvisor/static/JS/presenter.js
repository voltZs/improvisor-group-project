var asset;

var navigBar = document.getElementById("navigBar");

var timer = 0;
var timePassed = 0;


document.addEventListener("mousemove", function(){
    timer = 0;
    navigBar.classList.remove("hiddenNavigbar");
});

setInterval(function(){
    timer ++;
    if(timer>5) navigBar.classList.add("hiddenNavigbar");
}, 1000);

$(document).ready(function () {
    var socket = io();
    socket.emit('join');
    socket.on('presenter', function (receivedData) {
        console.log(receivedData);
        var directory = receivedData['assetLocation'];
        var temp = directory.split(".");
        var extension = temp[temp.length-1].toLowerCase();

        if(extension == "pdf"){
            $('#embed_display').attr('src', directory);
        } else {

        }

        $('#display').attr('src', directory);
    });
});
