


var formsContainer = document.getElementById("assetFormsContainer");
var firstFormClones = [];
$("#linkUploadFields1").hide();
$("#removeButton1").hide();
$("#assetLink").attr("id", "assetLink1");

firstFormClones.push(formsContainer.children[0].cloneNode(true));
var addAssetBtn = document.getElementById("addAssetBtn");
var submit = document.getElementById("submitButton");
var numOfForms = 1;

var currentAssetType = "file";

setEvents(1);
setStyling();


addAssetBtn.addEventListener("click", function(){
    firstFormClones.push(firstFormClones[numOfForms-1].cloneNode(true));
    firstFormClones[numOfForms-1].setAttribute("id", "form"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#fileUploadHidden1").attr("id", "fileUploadHidden"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#fileUploadVisible1").attr("id", "fileUploadVisible"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#thumbUploadHidden1").attr("id", "thumbUploadHidden"+(numOfForms+1));
    // $(firstFormClones[numOfForms-1]).find("#thumbUploadVisible1").attr("id", "thumbUploadVisible"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#fileUploadFields1").attr("id", "fileUploadFields"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#linkUploadFields1").attr("id", "linkUploadFields"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#assetLink1").attr("id", "assetLink"+(numOfForms+1));

    // chunk elowe prevents radio buttons from conflicting (label for : referst to input id)
    $(firstFormClones[numOfForms-1]).find("#assettype-0").parent().children().eq(1).attr("for", "#assettype-0-"+(numOfForms+1))
    $(firstFormClones[numOfForms-1]).find("#assettype-0").attr("id", "#assettype-0-"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#assettype-1").parent().children().eq(1).attr("for", "#assettype-1-"+(numOfForms+1))
    $(firstFormClones[numOfForms-1]).find("#assettype-1").attr("id", "#assettype-1-"+(numOfForms+1));

    $(firstFormClones[numOfForms-1]).find("#thumbnailSpace1").attr("id", "thumbnailSpace"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#hiddenField1").attr("id", "hiddenField"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#thumbHidden1").attr("id", "thumbHidden"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#thumbnailNameCheckbox1").attr("id", "thumbnailNameCheckbox"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#prevButton1").attr("id", "prevButton"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#nextButton1").attr("id", "nextButton"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#assetName1").attr("id", "assetName"+(numOfForms+1));

    $(firstFormClones[numOfForms-1]).find("#removeButton1").attr("id", "removeButton"+(numOfForms+1));

    formsContainer.appendChild(firstFormClones[numOfForms-1]);
    numOfForms++;
    setEvents(numOfForms);
    setStyling();
});

submitButton.addEventListener("click", function(){
    var all_valid = true;
    $("form").each(function(index){
        var valid = $("#form"+(index+1))[0].checkValidity();
        if(!valid){
            all_valid = false;
            $("#form"+(index+1)).find(':submit').click();
        }
    })

    if(all_valid ){
        $("form").each(function(index){
            if(index+1 == numOfForms){
                $("#form"+(index+1)).submit();
            } else {
                $("#form"+(index+1)).ajaxSubmit({url: '/assets/new', type: 'post'});
            }
        });
    };

});;

function setEvents(number){
    var fileVisibleButton = document.getElementById("fileUploadVisible"+(number));
    var fileHiddenButton = document.getElementById("fileUploadHidden"+(number));
    var thumbHiddenButton = document.getElementById("thumbUploadHidden"+(number));
    var thumbnailSpace = document.getElementById('thumbnailSpace'+ (number));
    var hiddenField = document.getElementById('thumbHidden' + (number));
    var fileButton = $("#form"+(number)).find("ul li:nth-child(1)");
    var linkButton = $("#form"+(number)).find("ul li:nth-child(2)");
    var fileUploadFields = $("#fileUploadFields"+(number));
    var linkUploadFields = $("#linkUploadFields"+(number));
    var assetLinkInput = document.getElementById("assetLink"+(number));
    var assetName = document.getElementById("assetName"+(number));
    var file;
    // PDF page buttons
    var prevButton =  document.getElementById('prevButton' + (number));
    var nextButton =  document.getElementById('nextButton' + (number));
    var thumbnailNameCheckboxCont = document.getElementById('thumbnailNameCheckbox' + (number));
    var thumbnailNameCheckbox = thumbnailNameCheckboxCont.children[0];
    var removeButton = document.getElementById('removeButton' + (number));

    $(removeButton).parent().hover(function(){
      $(removeButton).show();
    },
    function(){
      $(removeButton).hide();
    })

    removeButton.addEventListener("click", function(){
      $(removeButton).parent().remove();
    })

    $(thumbHiddenButton).hide();
    $(nextButton).hide();
    $(prevButton).hide();
    $(nextButton).parent().hide();
    $(thumbnailNameCheckboxCont).hide();
    fileVisibleButton.addEventListener("click", function(event){
        fileHiddenButton.click();
        event.stopPropagation();
    });

    thumbnailSpace.addEventListener("click", function(){
        thumbHiddenButton.click();
    })

    $(fileHiddenButton).change(function(){
        var valueArray = fileHiddenButton.value.split("\\");
        var value = valueArray[valueArray.length-1];
        fileVisibleButton.children[1].innerHTML = value;
    });

    fileButton.click(function(){
        $(this).children()[0].click();
        setStyling();

        fileUploadFields.show();
        linkUploadFields.hide();

        fileHiddenButton.required = true;
        assetLinkInput.removeAttribute("required");
        currentAssetType = "file";
    });

    linkButton.click(function(){
        $(this).children()[0].click();
        setStyling();

        fileUploadFields.hide();
        linkUploadFields.show();

        fileHiddenButton.removeAttribute("required");
        assetLinkInput.required = true;
        currentAssetType = "link";
    });

    assetLinkInput.addEventListener("change", function(){
        if(thumbnailNameCheckbox.checked == false){
            thumbnailFromAssetName(assetLinkInput.value, thumbnailSpace, hiddenField);
            $(thumbnailNameCheckboxCont).show();
        }
    })

    fileHiddenButton.addEventListener("change", function(){
        file = fileHiddenButton.files[0];
        createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton, number);
        $(thumbnailNameCheckboxCont).show();
    });

    thumbHiddenButton.addEventListener("change", function(){
        file = thumbHiddenButton.files[0];
        createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton, number);
        $(thumbnailNameCheckboxCont).show();
    });

    prevButton.addEventListener('click', function(event) {
        if(lastClickedPDF != number){
            showPDF(URL.createObjectURL(file), thumbnailSpace, hiddenField, nextButton, prevButton, number);
        } else {
            if(__CURRENT_PAGE > 0){
                showPage(--__CURRENT_PAGE, thumbnailSpace, hiddenField, nextButton, prevButton, number);
                createThumbnailPDF(thumbnailSpace, hiddenField);
            }
        }
    });

    nextButton.addEventListener('click', function() {
        if(lastClickedPDF != number){
            showPDF(URL.createObjectURL(file), thumbnailSpace, hiddenField, nextButton, prevButton);
        } else {
            if(__CURRENT_PAGE <= __TOTAL_PAGES){
                showPage(++__CURRENT_PAGE, thumbnailSpace, hiddenField, nextButton, prevButton);
                createThumbnailPDF(thumbnailSpace, hiddenField);
            }
        }
    });

    // function that updates the thumbnail if it is the name of the asses and
    // when it has been updated
    assetName.addEventListener('change', function(){
      // checks if the "use name as thumbnail" checkbox has been ticked before
      // updating the thumbnail
      if(thumbnailNameCheckbox.checked){
        $(nextButton).parent().hide();
        var name = document.getElementById('assetName' + (number)).value;
        thumbnailFromAssetName(name, thumbnailSpace, hiddenField);
      }
    });

    thumbnailNameCheckbox.addEventListener('change', function(){
      if(this.checked == true){
        console.log('The checkbox has been ticked');
        $(nextButton).parent().hide();
        var name = document.getElementById('assetName' + (number)).value;
        thumbnailFromAssetName(name, thumbnailSpace, hiddenField);
      }else{
        console.log('The checkbox has been unticked');
        $(nextButton).parent().show();
        thumbnailSpace.innerHTML= "";
        if(currentAssetType == "file")
            createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton);
        else
            thumbnailFromAssetName(assetLinkInput.value, thumbnailSpace, hiddenField);
      }
    });
}


function setStyling(){
    $("ul").attr("class", "no-bulletpoint midScreen");
    $("ul li").attr("class", "bubbleButton bubbleButtonWhite toggleButton");
    $('input[type="radio"]').parent().removeClass("selected");
    $('input[type="radio"]:checked').parent().addClass("selected");
}
