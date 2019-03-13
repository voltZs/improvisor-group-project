var textInputFilter = document.getElementById("tagTextInput");
var tagsContainer = document.getElementById("filterTagsContainter");
var tagset = fetchTagset();

var filterTags = [];
var sorting = 'recent';
var limit = 10;

var increment = 10;
var assetPool = document.getElementById("assetPool");
var moreAssetsButton = document.getElementById("loadMore");

var suggestions = document.getElementById("suggestions");
for(tag in tagset){
    var option = document.createElement("option");
    option.setAttribute("value", tagset[tag]);
    suggestions.appendChild(option);
}

var on_touchscreen = false;
var isExpanded = false;
var sortingDiv = document.getElementById("sortingDiv");
var sortingBtnsCont = document.getElementById("sortBtnContainer");
var sortBtnRecent = document.getElementById("sortBtnRecent");
var sortBtnOld = document.getElementById("sortBtnOld");
var sortBtnRelevant = document.getElementById("sortBtnRelevant");

var selectAssetsToggle = document.getElementById("selectAssetsToggle");
var selectAssetsDelete = document.getElementById("selectAssetsDelete");
selectAssetsDelete.hidden = true;
var toBeDeleted = [];

var selectionMode = false;

checkSorting();
checkIfNoData();
addThumbnailDeleteListeners();


selectAssetsToggle.addEventListener("click", function(){
    if(selectionMode){
        selectionMode = false;
        selectAssetsToggle.classList.remove("selected");
        selectAssetsDelete.hidden=true;
        removeSelections();
        toBeDeleted = [];
    } else {
        selectionMode = true;
        selectAssetsToggle.classList.add("selected");
    }

})

selectAssetsDelete.addEventListener("click", function(){
    $.ajax({
      type: "POST",
      url: "/assets/bulk_delete",
      data: {
        'idList': JSON.stringify(toBeDeleted)
      },
      timeout: 60000,
      success: function (data) {
          console.log("Deleted assets:" + JSON.parse(data));
          getAssets(filterTags, sorting, limit);
      }
    });
    toBeDeleted = [];
})

sortBtnRecent.addEventListener("click", function(event){
    if(!isExpanded){
        return;
    }
    isExpanded = false;
    sorting = "recent";
    checkSorting();
    getAssets(filterTags, sorting, limit);
    event.stopPropagation();
})
sortBtnOld.addEventListener("click", function(){
    if(!isExpanded){
        return;
    }
    isExpanded = false;
    sorting = "old";
    checkSorting();
    getAssets(filterTags, sorting, limit);
    event.stopPropagation();
})
sortBtnRelevant.addEventListener("click", function(){
    if(!isExpanded){
        return;
    }
    isExpanded = false;
    sorting = "relevant";
    checkSorting();
    getAssets(filterTags, sorting, limit);
    event.stopPropagation();
})

sortingDiv.addEventListener("mouseover", function(){
    if(!is_touch_device()){
        isExpanded = true;
    }
    console.log(isExpanded);
    sortBtnRecent.hidden = false;
    sortBtnOld.hidden = false;
    sortBtnRelevant.hidden = false;
})

sortingDiv.addEventListener("click", function(){
    if(is_touch_device()){
        isExpanded = true;
    }
    console.log(isExpanded);
    sortBtnRecent.hidden = false;
    sortBtnOld.hidden = false;
    sortBtnRelevant.hidden = false;
})

sortingDiv.addEventListener("mouseleave", function(){
    checkSorting()
    isExpanded = false;
})

function checkSorting(){

    sortBtnRecent.hidden = true;
    sortBtnOld.hidden = true;
    sortBtnRelevant.hidden = true;

    if(sorting == "recent"){
        sortBtnRecent.hidden = false;
        sortingBtnsCont.insertBefore(sortBtnRecent, sortingBtnsCont.children[0]);
    } else if(sorting == "old"){
        sortBtnOld.hidden = false;
        sortingBtnsCont.insertBefore(sortBtnOld, sortingBtnsCont.children[0]);
    } else if (sorting == "relevant"){
        sortBtnRelevant.hidden = false;
        sortingBtnsCont.insertBefore(sortBtnRelevant, sortingBtnsCont.children[0]);
    }
}



textInputFilter.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        getTagFromInput();
    }
});

checkLoadMoreBtn();

moreAssetsButton.addEventListener("click", function(){
    limit+= increment;
    getAssets(filterTags, sorting, limit);
})

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
        if(assetPool.children.length < limit){
            var newLimit = assetPool.children.length;
            if (newLimit >10){
                limit = newLimit;
            } else {
                limit = 10;
            }
        }
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

        data = JSON.parse(data);
        console.log(data);

        assetPool.innerHTML = "";
        for(var i=0; i<data.length; i++){
            if(!data[i] || i==limit){
                break;
            }
            var link = document.createElement("A");
            link.setAttribute("href", "/assets/" + data[i]["id"]);
            var div = document.createElement("DIV");
            div.classList.add("assetpool-asset");
            div.setAttribute('id', data[i]["id"]);
            var img = document.createElement("IMG");
            img.classList.add("assetThumbnail");
            img.setAttribute("src", data[i]["thumbnailLocation"]);
            var p = document.createElement("P");
            p.classList.add("blackText");
            p.classList.add("boldText");
            p.classList.add("labelText");
            p.innerHTML = data[i]["asset"]
            div.appendChild(img);
            div.appendChild(p);
            link.appendChild(div);
            link.addEventListener("click", function(event){
                if(selectionMode){
                    event.preventDefault();
                    console.log("Clicking button");
                }
            })
            assetPool.appendChild(link);
        }
        addThumbnailDeleteListeners();
        selectAssetsDelete.hidden = true;
        checkIfNoData();
        checkLoadMoreBtn();
      }
    });
}



function addThumbnailDeleteListeners(){
    for(var i =0; i< assetPool.children.length; i++){
        assetPool.children[i].addEventListener("click", function(event){
            if(selectionMode){
                event.preventDefault();
                var asset = this.children[0];
                var asset_id = parseInt(asset.getAttribute("id"), 10);
                if(toBeDeleted.includes(asset_id))
                    toBeDeleted.splice(toBeDeleted.indexOf(asset_id), 1);
                else
                    toBeDeleted.push(asset_id);
                if(toBeDeleted.length > 0)
                    selectAssetsDelete.hidden = false;
                else
                    selectAssetsDelete.hidden = true;
                asset.classList.toggle("selected");
            }
        })
    }
}

function removeSelections(){
    for(var i =0; i< assetPool.children.length; i++){
        var asset = assetPool.children[i].children[0];
        asset.classList.remove("selected");
    }
}

function checkIfNoData(){
    if(assetPool.children.length == 0){
        assetPool.innerHTML = "<br><h3>No assets matching your criteria</h3><br>";
    }
}

function checkLoadMoreBtn(){
    if(assetPool.children.length == limit){
        moreAssetsButton.style.display = "inline-block"
    } else {
        moreAssetsButton.style.display = "none"
    }
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

function is_touch_device() {
 return (('ontouchstart' in window)
      || (navigator.MaxTouchPoints > 0)
      || (navigator.msMaxTouchPoints > 0));
}

// window.addEventListener('touchstart', function(){
//     on_touchscreen = true;
// })
