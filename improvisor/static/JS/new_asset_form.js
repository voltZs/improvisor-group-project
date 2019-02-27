var formsContainer = document.getElementById("assetFormsContainer");
var firstFormClones = [];
firstFormClones.push(formsContainer.children[0].cloneNode(true));
var addAssetBtn = document.getElementById("addAssetBtn");
var submit = document.getElementById("submitButton");
var numOfForms = 1;

setEvents(1);

addAssetBtn.addEventListener("click", function(){
    firstFormClones.push(firstFormClones[numOfForms-1].cloneNode(true));
    firstFormClones[numOfForms-1].setAttribute("id", "form"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#fileUploadHidden1").attr("id", "fileUploadHidden"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#fileUploadVisible1").attr("id", "fileUploadVisible"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#thumbUploadHidden1").attr("id", "thumbUploadHidden"+(numOfForms+1));
    $(firstFormClones[numOfForms-1]).find("#thumbUploadVisible1").attr("id", "thumbUploadVisible"+(numOfForms+1));

    formsContainer.appendChild(firstFormClones[numOfForms-1]);
    numOfForms++;
    setEvents(numOfForms);
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
    fileVisibleButton.addEventListener("click", function(event){
        document.getElementById("fileUploadHidden"+(number)).click();
        event.stopPropagation();
    });

    var thumbVisibleButton = document.getElementById("thumbUploadVisible"+(number));
    thumbVisibleButton.addEventListener("click", function(){
        document.getElementById("thumbUploadHidden"+(number)).click();
    });
}
