// shows the microphone button to test tags
document.getElementById('thumbnailTestMic').classList.remove('hidden');


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

  microphoneToggle.addEventListener('click', function () {
    if (listening) {
      stopListening();
      console.log('listening is set to:' + listening);
    } else {
      console.log('listening is set to:' + listening);
      startListening();
      console.log('listening is set to:' + listening);
    }
  });

}

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
