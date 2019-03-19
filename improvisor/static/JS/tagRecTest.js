// shows the microphone button to test tags
var micIcon = document.getElementById('thumbnailTestMic');
micIcon.classList.remove('hidden');



// Annyang for checking tags

var listening = false;
tagSpeechText = document.getElementById('tagSpeechOutput');
microphoneToggle = document.getElementById("microphoneIcon");
microphoneIcon = document.getElementById('microphoneIcon');
if (annyang) {

  annyang.addCallback('result', function (phrases) {
    var text = phrases[0];
    text = text.toLowerCase();

    console.log("Recognized text: ", text);
    tagSpeechText.value = text;


  });

  annyang.addCallback('end', function () {
    // if (recognisedTagsUsed.length != 0) {
    //   //recognisedTagsUsed = [];
    // }
  });
  // Start listening. You can call this here, or attach this call to an event, button, etc.


}
var microphone = document.getElementById("microphoneIcon");
microphoneToggle.addEventListener('click', function () {
  if (listening) {
    stopListening();
    microphone.setAttribute('data-original-title', " Test speech recognition for better tag selection");
  } else {
    startListening();
    $("[data-toggle='tooltip']").tooltip('hide');
    microphone.setAttribute('data-original-title', "");

  }
});

function startListening() {
  //noSleep.enable();
  annyang.start({
    autoRestart: true,
    continuous: false
  });
  var recognition = annyang.getSpeechRecognizer();
  recognition.interimResults = true;
  console.log("Started listening");

  microphoneIcon.classList.add("fa-microphone");
  microphoneIcon.classList.remove("fa-microphone-slash");
  tagSpeechText.classList.remove("hidden");
  microphoneIcon.title = "";
  document.getElementById("microphoneIcon").title = "";
  listening = true;
}

function stopListening() {
  if (listening) {
    console.log("Stopped listening");
  }
  //noSleep.disable();
  annyang.abort()
  microphoneIcon.classList.add("fa-microphone-slash");
  microphoneIcon.classList.remove("fa-microphone");
  tagSpeechText.classList.add("hidden");
  tagSpeechText.value="";
  listening = false;
}



$(function(){
  $('[data-toggle="tooltip"]').tooltip()
});


$(function(){
  if(isPressed){
    $('[data-toggle="tooltip"]').click(function(){
      $('[data-toggle="tooltip"]').tooltip("hide");
    })
  }else{
    $('[data-toggle="tooltip"]').click(function(){
      $('[data-toggle="tooltip"]').tooltip("show");
    })
  }

});
