var profileImgBtn = document.getElementById("profileImgBtn");
var userPictureInput = document.getElementById("userPicture");
var resetColorBtn = document.getElementById("resetColor");

$(userPictureInput).parent().hide();

profileImgBtn.addEventListener("click", function(){
  userPictureInput.click();
})

userPictureInput.addEventListener("change", function(){
  document.getElementById("userForm").submit();
})

resetColorBtn.addEventListener("click", function(){
  document.getElementById("colourSetting").value = "#2664c9";
})
