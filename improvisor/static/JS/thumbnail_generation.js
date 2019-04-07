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
  thumbnail.src = canvas.toDataURL('image/png', 2);


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
