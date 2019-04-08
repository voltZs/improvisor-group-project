var profileImgBtn = document.getElementById("profileImgBtn");
var userPictureInput = document.getElementById("userPicture");

$(userPictureInput).parent().hide();

profileImgBtn.addEventListener("click", function(){
  userPictureInput.click();
})

userPictureInput.addEventListener("change", function(){
  document.getElementById("userForm").submit();
})
