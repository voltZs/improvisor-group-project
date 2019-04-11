$("#modalHelpIcon").show();

var modalHelp = document.getElementById('helpModal');

// gets the link to the modal
var linkHelp = document.getElementById("modalHelpIcon");

// Get the <span> element that closes the modal
var spanHelp = document.getElementsByClassName("closeHelp")[0];



// When the user clicks on the link, open the modal
linkHelp.onclick = function() {
  modalHelp.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
spanHelp.onclick = function() {

  modalHelp.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modalHelp) {
    modalHelp.style.display = "none";
  }
}
