

var assetTags = [];

var assetNameInput = document.getElementById("assetNameInput");

var textInputFilter = document.getElementById("tagTextInput");
var tagsContainer = document.getElementById("assetTagsContainter");
var tagset = fetchTagset();

var deleteButton = document.getElementById("asset-delete");
var saveButton = document.getElementById("asset-save");
var assetID = parseInt($("#hidden-id-data").attr("data"));
document.getElementById("inputTagArray").hidden = true;

var thumbnailSpace = document.getElementById('thumbnailSpace');
var hiddenField = document.getElementById('thumbHidden');
var file;
var thumbnailImage = document.getElementById("thumbnailImg");
var thumbnailUploadHidden = document.getElementById("thumbUploadHidden");
var prevButton =  document.getElementById('prevButton');
var nextButton =  document.getElementById('nextButton');
var thumbnailNameCheckboxCont = document.getElementById('thumbnailNameCheckbox');
var thumbnailNameCheckbox = thumbnailNameCheckboxCont.children[0];

$(".hidden-tags-data").each(function(){
    var tag =$(this).attr("data");
    addTagElement(tag);
})
var suggestions = document.getElementById("suggestions");
for(tag in tagset){
    var option = document.createElement("option");
    option.setAttribute("value", tagset[tag]);
    suggestions.appendChild(option);
}

textInputFilter.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        getTagFromInput();
    }
});

function getTagFromInput(){
    var newTag = textInputFilter.value;
    var inArray = false;
    for(var i= 0; i< assetTags.length; i++){
        if(assetTags[i].toLowerCase() == newTag.toLowerCase())
            inArray = true;
    }
    if(!inArray){
        addTagElement(newTag);
    }
    textInputFilter.value = "";
}
function addTagElement(newTag){
    assetTags.push(newTag);
    var tagButton = document.createElement("DIV");
    tagButton.classList.add("filterTagButton");
    var holderSpan = document.createElement("SPAN");
    holderSpan.innerHTML = newTag;
    var toggleSpan = document.createElement("SPAN");
    toggleSpan.classList.add("removeToggle");
    toggleSpan.innerHTML = "<i class='fas fa-times'></i>";

    tagButton.appendChild(holderSpan);
    tagButton.appendChild(toggleSpan);

    //add event listener for remove button
    toggleSpan.addEventListener("click", function(){
        var index = assetTags.indexOf(newTag);
        if (index > -1) {
           assetTags.splice(index, 1);
        }
        tagButton.parentNode.removeChild(tagButton);
    })
    assetTagsContainter.appendChild(tagButton);
}

$(nextButton).hide();
$(prevButton).hide();
thumbnailSpace.addEventListener("click", function(){
    thumbnailUploadHidden.click();
})

thumbnailUploadHidden.addEventListener("change", function(){
    file = thumbnailUploadHidden.files[0];
    createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton, 1);
    $(thumbnailNameCheckboxCont).show();
});

prevButton.addEventListener('click', function(event) {
    if(lastClickedPDF != 1){
        showPDF(URL.createObjectURL(file), thumbnailSpace, hiddenField, nextButton, prevButton, 1);
    } else {
        if(__CURRENT_PAGE > 0){
            showPage(--__CURRENT_PAGE, thumbnailSpace, hiddenField, nextButton, prevButton, 1);
            createThumbnailPDF(thumbnailSpace, hiddenField);
        }
    }
});

nextButton.addEventListener('click', function() {
    if(lastClickedPDF != 1){
        showPDF(URL.createObjectURL(file), thumbnailSpace, hiddenField, nextButton, prevButton);
    } else {
        if(__CURRENT_PAGE <= __TOTAL_PAGES){
            showPage(++__CURRENT_PAGE, thumbnailSpace, hiddenField, nextButton, prevButton);
            createThumbnailPDF(thumbnailSpace, hiddenField);
        }
    }
});

// function that updates the thumbnail if it is the name of the assets and
// when it has been updated
assetNameInput.addEventListener('change', function(){
  // checks if the "use name as thumbnail" checkbox has been ticked before
  // updating the thumbnail
  if(thumbnailNameCheckbox.checked){
    $(nextButton).parent().hide();
    var name = assetNameInput.value;
    thumbnailFromAssetName(name, thumbnailSpace, hiddenField);
  }
});

thumbnailNameCheckbox.addEventListener('change', function(){
  if(this.checked == true){
    console.log('The checkbox has been ticked');
    $(nextButton).parent().hide();
    var name = assetNameInput.value;
    thumbnailFromAssetName(name, thumbnailSpace, hiddenField);
  }else{
    console.log('The checkbox has been unticked');
    $(nextButton).parent().show();
    thumbnailSpace.innerHTML= "";
    createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton);

  }
});





deleteButton.addEventListener("click", function(){
    $.ajax({
      type: "POST",
      url: "/assets/" + assetID + "/delete",
      timeout: 60000,
      success: function (data) {
        var retrieved = JSON.parse(data);
        if(retrieved['success'])
            window.location.replace("/assets");
        else
            console.log("Could not delete the asset id");
      }
    });
})

saveButton.addEventListener("click", function(){
    var stringArray = "";
    for(var i=0; i<assetTags.length; i++){
        if(i==assetTags.length-1)
            stringArray += assetTags[i];
        else
            stringArray += assetTags[i] + ",";
    }
    document.getElementById("inputTagArray").value = stringArray;
    document.getElementById("formUpdate").submit();
})


function fetchTagset(){
  var tmp = null;
  $.ajax({
    async: false,
    url: "/fetch_tagset",
    timeout: 60000,
    success: function (data) {
      tmp = JSON.parse(data);
    }
  });
  return tmp;
}
