$("#modalHelpIcon").show();

var modal = document.getElementById('helpModal');

// gets the link to the modal
var link = document.getElementById("modalHelpIcon");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("closeHelp")[0];



// When the user clicks on the link, open the modal
link.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {

  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
