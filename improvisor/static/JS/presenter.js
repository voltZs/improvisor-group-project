var asset;

$(document).ready(function () {
    var socket = io();
    socket.emit('join');
    socket.on('presenter', function (receivedData) {
        console.log(receivedData);
        var directory = receivedData['assetLocation'];
        $('#display').attr('src', directory);
    });
});
