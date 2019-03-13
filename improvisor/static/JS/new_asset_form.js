var formsContainer = document.getElementById("assetFormsContainer");
var firstFormClones = [];
$("#linkUploadFields1").hide();
firstFormClones.push(formsContainer.children[0].cloneNode(true));
var addAssetBtn = document.getElementById("addAssetBtn");
var submit = document.getElementById("submitButton");
var numOfForms = 1;

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

    // chunk elowe prevents radio buttons from conflicting (label for : referst to input id)
    $(firstFormClones[numOfForms-1]).find("#assettype-0").parent().children().eq(1).attr("for", "#assettype-0-"+(numOfForms+1))
    $(firstFormClones[numOfForms-1]).find("#assettype-0").attr("id", "#assettype-0-"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#assettype-1").parent().children().eq(1).attr("for", "#assettype-1-"+(numOfForms+1))
    $(firstFormClones[numOfForms-1]).find("#assettype-1").attr("id", "#assettype-1-"+(numOfForms+1));

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
    fileVisibleButton.addEventListener("click", function(event){
        fileHiddenButton.click();
        event.stopPropagation();
    });

    $(fileHiddenButton).change(function(){
        var valueArray = fileHiddenButton.value.split("\\");
        var value = valueArray[valueArray.length-1];
        fileVisibleButton.children[1].innerHTML = value;
    });

    var fileButton = $("#form"+(number)).find("ul li:nth-child(1)");
    var linkButton = $("#form"+(number)).find("ul li:nth-child(2)");
    var fileUploadFields = $("#fileUploadFields"+(number));
    var linkUploadFields = $("#linkUploadFields"+(number));

    fileButton.click(function(){
        $(this).children()[0].click();
        setStyling();
        fileUploadFields.show();
        linkUploadFields.hide();
    });

    linkButton.click(function(){
        $(this).children()[0].click();
        setStyling();
        fileUploadFields.hide();
        linkUploadFields.show();
    });

    // var thumbVisibleButton = document.getElementById("thumbUploadVisible"+(number));
    // var thumbHiddenButton = document.getElementById("thumbUploadHidden"+(number));
    // thumbVisibleButton.addEventListener("click", function(){
    //     thumbHiddenButton.click();
    // });
}


function setStyling(){
    $("ul").attr("class", "no-bulletpoint midScreen");
    $("ul li").attr("class", "bubbleButton bubbleButtonWhite toggleButton");
    $('input[type="radio"]').parent().removeClass("selected");
    $('input[type="radio"]:checked').parent().addClass("selected");
}
