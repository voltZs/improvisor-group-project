var sorting = document.getElementById("data-sorting").getAttribute("data");
if (sorting != 'recent' && sorting != 'old'){
  sorting = 'recent';
};
var sortingDiv = document.getElementById("sortingDiv");
var sortingBtnsCont = document.getElementById("sortBtnContainer");
var sortBtnRecent = document.getElementById("sortBtnRecent");
var sortBtnOld = document.getElementById("sortBtnOld");

var isExpanded = false;

checkSorting();


sortBtnRecent.addEventListener("click", function(event){
    if(!isExpanded){
        return;
    }
    isExpanded = false;
    sorting = "recent";
    checkSorting();
    event.stopPropagation();
    window.location.replace("/sessions?sorting=" + sorting);
})
sortBtnOld.addEventListener("click", function(){
    if(!isExpanded){
        return;
    }
    isExpanded = false;
    sorting = "old";
    checkSorting();
    event.stopPropagation();
    window.location.replace("/sessions?sorting=" + sorting);
})

sortingDiv.addEventListener("mouseover", function(){
    if(!is_touch_device()){
        isExpanded = true;
    }
    console.log(isExpanded);
    sortBtnRecent.hidden = false;
    sortBtnOld.hidden = false;
})

sortingDiv.addEventListener("click", function(){
    if(is_touch_device()){
        isExpanded = true;
    }
    console.log(isExpanded);
    sortBtnRecent.hidden = false;
    sortBtnOld.hidden = false;
})

sortingDiv.addEventListener("mouseleave", function(){
    isExpanded = false;
    checkSorting();
})



function checkSorting(){
    sortBtnRecent.hidden = true;
    sortBtnOld.hidden = true;

    if(sorting == "recent"){
        sortBtnRecent.hidden = false;
        sortingBtnsCont.insertBefore(sortBtnRecent, sortingBtnsCont.children[0]);
    } else if(sorting == "old"){
        sortBtnOld.hidden = false;
        sortingBtnsCont.insertBefore(sortBtnOld, sortingBtnsCont.children[0]);
    }
}

function is_touch_device() {
 return (('ontouchstart' in window)
      || (navigator.MaxTouchPoints > 0)
      || (navigator.msMaxTouchPoints > 0));
}
