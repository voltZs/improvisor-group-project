$(document).ready(function () {
    var socket = io();
    socket.on('presenter', function (filename) {
        var directory = "/static/resources/images/"
        var file = directory + filename + ".jpg";
        $('#display').attr('src', file);
        console.log('Received ID ' + filename);
    });
});
