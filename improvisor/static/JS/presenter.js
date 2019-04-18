var asset;

$('.backgroundMotive').hide();

var navigBar = document.getElementById("navigBar");
var presenterView = document.getElementById("presenterView");
var defaultView = document.getElementById("presenterDefault");
emptyViews();

var timer = 0;
var timePassed = 0;

var textFormats = ["txt", "csv"];
var imageFormats = ["jpg", "jpeg", "png", "bmp", "tiff"];

var bckgrnd_color = document.getElementById("data-color").getAttribute("data");
var bckgrnd_rgb = hexToRgb(bckgrnd_color);
var perc_bright = ((bckgrnd_rgb['r']*299) + (bckgrnd_rgb['g']*587) + (bckgrnd_rgb['b']*114)) / 1000;
if(perc_bright>150){
  $(defaultView.children).css("color", "black");
} else {
  $(defaultView.children).css("color", "white");
}
var lastAssetDiv = document.getElementById("data-lastAssetData");
var lastAssetDivData = lastAssetDiv.getAttribute("data");
if(lastAssetDivData){
  $(defaultView).hide();
  var lastAsset = JSON.parse(lastAssetDivData);
  showAsset(lastAsset);
} else {
  $(presenterView).hide();
}

$("html").css("background", "none");
$("html").css("background-color", bckgrnd_color );

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
    socket.on('presenter', function (data) {
        $(presenterView).show();
        $(defaultView).hide();
        emptyViews();
        showAsset(data)
    });
});

function showAsset(receivedData){
  if (receivedData['assettype'] == "file"){
      var directory = receivedData['assetLocation'];
      var temp = directory.split(".");
      var extension = temp[temp.length-1].toLowerCase();

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
  } else if(receivedData['assettype'] == "link"){
      $('#link_display').show();
      $('#link_display').html(receivedData['assetLink']);
      $('#link_display').attr('href', "//" + receivedData['assetLink']);
  }
}

function emptyViews(){
    $(presenterView.children).attr("src", "");
    $(presenterView.children).attr("data", "");
    $(presenterView.children).attr("href", "");
    $(presenterView.children).html("");
    $(presenterView.children).hide();
}

function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}
