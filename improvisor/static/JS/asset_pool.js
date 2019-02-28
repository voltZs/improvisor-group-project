var textInputFilter = document.getElementById("tagTextInput");
var tagsContainer = document.getElementById("filterTagsContainter");
var tagset = fetchTagset();

var filterTags = [];
var sorting = 'recent';
var limit = 5;

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
    if(filterTags.indexOf(newTag) == -1){
        addTagElement(newTag);
    }
    textInputFilter.value = "";
    getAssets(filterTags, sorting, limit);
}

function addTagElement(newTag){
    filterTags.push(newTag);
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
        var index = filterTags.indexOf(newTag);
        if (index > -1) {
           filterTags.splice(index, 1);
        }
        tagButton.parentNode.removeChild(tagButton);
        getAssets(filterTags, sorting, limit);
    })

    filterTagsContainter.appendChild(tagButton);
}

function getAssets(tags, sorting, limit){
    $.ajax({
      type: "POST",
      url: "/assets/select",
      data: {
        'filterTags': JSON.stringify(tags),
        'sorting': sorting,
        'limit': limit
      },
      timeout: 60000,
      success: function (data) {
        console.log(data)
      }
    });
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
