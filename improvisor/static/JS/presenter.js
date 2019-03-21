var asset;

var navigBar = document.getElementById("navigBar");
var presenterView = document.getElementById("presenterView")
emptyViews();

var timer = 0;
var timePassed = 0;

var textFormats = ["txt", "csv"];


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

        emptyViews();

        if(extension == "pdf"){
            $('#embed_display').show();
            $('#embed_display').attr('src', directory);
        } else if (textFormats.includes(extension)) {
            $('#object_display').show();
            $('#object_display').attr('data', directory);
        } else if (imageFormats.includes(extension)) {
            $('#img_display').show();
            $('#img_display').attr('src', directory);
        }


    });
});

function emptyViews(){
    $(presenterView.children).attr("src", "");
    $(presenterView.children).attr("data", "");
    $(presenterView.children).hide();
}
