var assetTags = [];

var textInputFilter = document.getElementById("tagTextInput");
var tagsContainer = document.getElementById("assetTagsContainter");
var tagset = fetchTagset();

$(".hidden-data").each(function(){
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
    newTag = textInputFilter.value;
    if(assetTags.indexOf(newTag) == -1){
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

function saveChanges(){

}


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
