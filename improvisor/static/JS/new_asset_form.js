


var formsContainer = document.getElementById("assetFormsContainer");
var firstFormClones = [];
$("#linkUploadFields1").hide();
$("#assetLink").attr("id", "assetLink1");

firstFormClones.push(formsContainer.children[0].cloneNode(true));
var addAssetBtn = document.getElementById("addAssetBtn");
var submit = document.getElementById("submitButton");
var numOfForms = 1;

var lastClickedPDF;
// CREDIT TO USEFUL ANGLE
// source : http://usefulangle.com/post/20/pdfjs-tutorial-1-preview-pdf-during-upload-wih-next-prev-buttons

// creating variables used
var __PDF_DOC; // will hold the P?DFDocumentProxy object that is passed into the
// callback of the getDocumentPromise
var __CURRENT_PAGE; // will hole the current page number.
var __TOTAL_PAGES; // will old the total no of pages
var __PAGE_RENDERING_IN_PROGRESS = 0; // is a flag that will hold whether a
// currently being rendered or not. if rendering is in pgogress Previous & next buttons will be disabled
var __CANVAS = document.createElement('canvas');
var __CANVAS_CTX = __CANVAS.getContext('2d');


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
    $(firstFormClones[numOfForms-1]).find("#assetLink").attr("id", "assetLink"+(numOfForms+1));

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
    var file;
    // PDF page buttons
    var prevButton =  document.getElementById('prevButton' + (number));
    var nextButton =  document.getElementById('nextButton' + (number));
    var thumbnailNameCheckboxCont = document.getElementById('thumbnailNameCheckbox' + (number));
    var thumbnailNameCheckbox = thumbnailNameCheckboxCont.children[0];

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
    });

    linkButton.click(function(){
        $(this).children()[0].click();
        setStyling();

        fileUploadFields.hide();
        linkUploadFields.show();

        fileHiddenButton.removeAttribute("required");
        assetLinkInput.required = true;
    });

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

    thumbnailNameCheckbox.addEventListener('change', function(){
      if(this.checked == true){
        console.log('The checkbox has been ticked');
        $(nextButton).parent().hide();
        //gets the text from the asset name text input
        //######################
        //#  assetname         #
        //######################
        var name = document.getElementById('assetName' + (number)).value;
        thumbnailFromAssetName(name, thumbnailSpace, hiddenField);
      }else{
        console.log('The checkbox has been unticked');
        $(nextButton).parent().show();
        thumbnailSpace.innerHTML= "";
        createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton);
      }
    });
}


function setStyling(){
    $("ul").attr("class", "no-bulletpoint midScreen");
    $("ul li").attr("class", "bubbleButton bubbleButtonWhite toggleButton");
    $('input[type="radio"]').parent().removeClass("selected");
    $('input[type="radio"]:checked').parent().addClass("selected");
}


// ################## Thumbnail Generation ################

// creates a thumbnail from the uploaded file (png or pdf)
function createThumbnail(file, thumbnailSpace, hiddenField, nextButton, prevButton, id){

  var reader = new FileReader();
  reader.addEventListener("load", function(){
    //creates a temporary img element that will hold the downloaded image
    // which will then be resized using canvas and the resized image will be
    // displayed
    var image = document.createElement('img');
    image.src = reader.result;

    if(file.type ==='application/pdf'){
        $(nextButton).parent().show();
        $(nextButton).show();
        $(prevButton).show();
        showPDF(URL.createObjectURL(file), thumbnailSpace, hiddenField, nextButton, prevButton, id);
    }else if (file.type ==='image/jpeg' || file.type ==='image/png') {
      createThumbnailFromImage(image.src, thumbnailSpace, hiddenField);
      $(nextButton).hide();
      $(prevButton).hide();
    }
  }, false);

  if(file){
    reader.readAsDataURL(file);
  }
}


function resizeUsingCanvas(image) {
  var canvas, ctx, thumbnail, thumbnailScale, thumbnailWidth, thumbnailHeight;
  // setting the size of the thumbnail
  var thumbnailMaxWidth = 420;
  var thumbnailMaxHeight = 280;
  // create an off-screen canvas
  canvas = document.createElement('canvas');
  ctx = canvas.getContext('2d');

  //Calculate the size of the thumbnail, to best fit within max/width (cropspadding)
  thumbnailScale = (image.width / image.height) > (thumbnailMaxWidth / thumbnailMaxHeight) ?
  thumbnailMaxWidth / image.width :
  thumbnailMaxHeight / image.height;
  thumbnailWidth = image.width * thumbnailScale;
  thumbnailHeight = image.height * thumbnailScale;

  // set its dimension to target size
  canvas.width = thumbnailWidth;
  canvas.height = thumbnailHeight;

  // draw source image into the off-screen canvas:
  ctx.drawImage(image, 0, 0, thumbnailWidth, thumbnailHeight);

  // encode image to data-uri with base64 version of compressed image
  thumbnail = new Image();
  thumbnail.src = canvas.toDataURL('image/peg', 2);


  return thumbnail;
};



//creates a thumbnail from image source
function createThumbnailFromImage(imageSource, thumbnailSpace, hiddenField){
  // creates a variable to hold the original image
  var originalImage = new Image();
  // assigns the source of the original image
  originalImage.src = imageSource;
  // function that makes sure that the resto of the code executes once the
  // image finished loading
  originalImage.addEventListener("load", function () {
    var thumbnailImage = resizeUsingCanvas(originalImage);
    populateThumbnail(thumbnailImage, thumbnailSpace, hiddenField);
  });

}

function populateThumbnail(thumbnail, thumbnailSpace, hiddenField){

  thumbnail.classList.add('smallBox');

  // if there is already a thumbnail in the space, remove it before adding new
  thumbnailSpace.innerHTML=""

  // add the image to be displayed to the div
  thumbnailSpace.appendChild(thumbnail);
  hiddenField.setAttribute("value", thumbnail.src);
}





//######################### PDF ##############################

// Initialize and load the PDF
function showPDF(pdf_url, thumbnailSpace, hiddenField, nextButton, prevButton, id) {

  PDFJS.getDocument({ url: pdf_url }).then(function(pdf_doc) {
    __PDF_DOC = pdf_doc;
    __TOTAL_PAGES = __PDF_DOC.numPages;
    prev_pdf_ulr = pdf_url;

    lastClickedPDF = id;

    // Show the first page
    showPage(1, thumbnailSpace, hiddenField, nextButton, prevButton);

  }).catch(function(error) {

    alert(error.message);
  });;
}

// Load and render a specific page of the PDF
function showPage(page_no, thumbnailSpace, hiddenField, nextButton, prevButton) {
  __PAGE_RENDERING_IN_PROGRESS = 1;
  __CURRENT_PAGE = page_no;

  // Fetch the page
  __PDF_DOC.getPage(page_no).then(function(page) {
    // As the canvas is of a fixed width we need to set the scale of the viewport accordingly
    var scale_required = __CANVAS.width / page.getViewport(1).width;

    // Get viewport of the page at required scale
    var viewport = page.getViewport(scale_required);

    // Set canvas height
    __CANVAS.height = viewport.height;

    var renderContext = {
      canvasContext: __CANVAS_CTX,
      viewport: viewport
    };

    // Render the page contents in the canvas
    page.render(renderContext).then(function() {
      __PAGE_RENDERING_IN_PROGRESS = 0;

      createThumbnailPDF(thumbnailSpace, hiddenField);
      nextButton.classList.remove('hidden');
      prevButton.classList.remove('hidden');
    });
  });
}


function createThumbnailPDF(thumbnailSpace, hiddenField){
  thumbnail = new Image();
  thumbnail.src = __CANVAS.toDataURL('image/peg', 1);
  populateThumbnail(thumbnail, thumbnailSpace, hiddenField);
}


function thumbnailFromAssetName(name, thumbnailSpace, hiddenField){
  var canvas = document.createElement('canvas');
  canvas.width = 150;
  canvas.height = 150;
  var ctx = canvas.getContext('2d');
  ctx.fillStyle = "white";
  ctx.fillRect(0,0, canvas.width, canvas.height);
  var fontSize = 25;
  var width = 150; //width of the canvas
  ctx.fillStyle = 'black';
  ctx.font = fontSize + 'px Arial'; // font can be changed here
  wrapText (ctx, name, 5, 40, 148, 36)

  thumbnail = new Image();
  thumbnail.src = canvas.toDataURL('image/peg', 1);
  populateThumbnail(thumbnail, thumbnailSpace, hiddenField);

}


//CREDIT TO PETER HRYNKOW
//SOURCE: https://codepen.io/peterhyr/pen/AGIEa
// wraps text on canvas
function wrapText (context, text, x, y, maxWidth, lineHeight) {

  var words = text.split(' '),
  line = '',
  lineCount = 0,
  i,
  test,
  metrics;

  for (i = 0; i < words.length; i++) {
    test = words[i];
    metrics = context.measureText(test);
    while (metrics.width > maxWidth) {
      // Determine how much of the word will fit
      test = test.substring(0, test.length - 1);
      metrics = context.measureText(test);
    }
    if (words[i] != test) {
      words.splice(i + 1, 0,  words[i].substr(test.length))
      words[i] = test;
    }

    test = line + words[i] + ' ';
    metrics = context.measureText(test);

    if (metrics.width > maxWidth && i > 0) {
      context.fillText(line, x, y);
      line = words[i] + ' ';
      y += lineHeight;
      lineCount++;
    }
    else {
      line = test;
    }
  }

  context.fillText(line, x, y);
}
