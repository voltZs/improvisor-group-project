var sessionNameInput = document.getElementById("sessionNameInput");
var saveButton = document.getElementById("session-save");
var exportButton = document.getElementById("session-export");
var deleteButton = document.getElementById("session-delete");
var sessionID = parseInt($(".session-page").attr("id"));

applyGestureControls();

// function that updates the thumbnail if it is the name of the assets and
// when it has been updated
sessionNameInput.addEventListener('change', function () {
  // checks if the "use name as thumbnail" checkbox has been ticked before
  // updating the thumbnail
  var name = sessionNameInput.value;
});

saveButton.addEventListener("click", function () {
  document.getElementById("formUpdate").submit();
});

function getSessionAssets() {
  var tmp = null;
  $.ajax({
    async: false,
    url: "/sessions/" + sessionID + "/assets",
    timeout: 60000,
    success: function (data) {
      tmp = data;
    }
  });
  return tmp;
}

function getSessionInfo() {
  var tmp = null;
  $.ajax({
    async: false,
    url: "/sessions/" + sessionID + "/info",
    timeout: 60000,
    success: function (data) {
      tmp = data;
    }
  });
  return tmp;
}

exportButton.addEventListener("click", function () {
  event.preventDefault();

  var assets = getSessionAssets();
  var info = getSessionInfo();
  exportSlides(info, assets);
});

// Setup canvas for base 64 image conversion
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");

function convertImgToBase64(img, outputFormat) {
  if (img.assettype == "link") {
    return ""
  }
  // Set the canvas size to the image size
  canvas.width = img.width;
  canvas.height = img.height;
  // Add the image to the canvas
  ctx.drawImage(img, 0, 0);
  // Return the base64 version of the canvas
  return canvas.toDataURL("image/" + (outputFormat || "png"));
}

function getFileExtension(filename) {
  return filename.split('.').pop();
}

function exportSlides(info, assets) {
  // jsPDF Library - format is currently set to 1920x1080 (in mm)
  var doc = new jsPDF({
    orientation: 'landscape',
    unit: 'mm',
    format: [508, 285.75]
  });

  doc.setFont("times");
  doc.setFontStyle("normal");
  doc.setFontSize(30);
  // Horizontally center text on the PDF
  var centeredText = function (text, y) {
    var textWidth = doc.getStringUnitWidth(text) * doc.internal.getFontSize() / doc.internal.scaleFactor;
    var textOffset = (doc.internal.pageSize.width - textWidth) / 2;
    doc.text(textOffset, y, text);
  }
  // Horizontally center images on the PDF
  var centeredImage = function (img, type, marginTop, width, height) {
    var imageOffset = (doc.internal.pageSize.width - width) / 2;
    doc.addImage(img, type, imageOffset, marginTop, width, height);
  }

  // Display the session name and session author (first name + lastname)
  centeredText(info.sessionName, 50);
  doc.setFontSize(20);
  centeredText(info.sessionAuthor, 60);
  var slides = [];
  var pdfs = [];
  for (var i = 0; i < assets.length; i++) {
    // Store the asset details in the image object (even if it is a link instead of a file)
    var obj = new Image();
    obj.id = assets[i].asset_id;
    obj.assettype = assets[i].asset.assettype;
    obj.assetname = assets[i].asset.assetname;
    obj.thumbnail = assets[i].asset.thumbnailLocation;
    obj.link = assets[i].asset.assetLink;
    obj.date = assets[i].dateAdded
    obj.crossOrigin = "Anonymous";
    // Callback for when the source has loaded (obj.src = x)
    obj.onload = function () {
      if (this.assettype == "file") {
        // If it is a PDF, show the thumbnail of the PDF on the slide
        if (this.extension == "pdf") {
          var current = {
            src: this.thumbnail,
            asset_id: this.id,
            assettype: this.assettype,
            extension: this.extension,
            pdf: this.pdf,
            assetname: this.assetname,
            link: this.link,
            dateAdded: this.date,
            base64: convertImgToBase64(this),
            width: this.width,
            height: this.height
          };
          slides.push(current);
          pdfs.push(current);
        } else {
          var current = {
            src: this.src,
            asset_id: this.id,
            assettype: this.assettype,
            link: this.link,
            dateAdded: this.date,
            base64: convertImgToBase64(this),
            width: this.width,
            height: this.height
          };
          slides.push(current);
        }
      } else if (this.assettype == "link") {
        slides.push({
          asset_id: this.id,
          assettype: this.assettype,
          link: this.link,
          dateAdded: this.date,
        });
      }

      // If all the images have loaded
      // (which means this gets run after the last image is pushed)
      if (slides.length === assets.length) {
        // Sort the list by date
        slides.sort(function (a, b) {
          return new Date(a.dateAdded) - new Date(b.dateAdded);
        });
        // Add the asset to the PDF
        for (var j = 0; j < slides.length; j++) {
          doc.addPage();
          if (slides[j].assettype == "file") {
            // Maximum width and height for asset output (in mm)
            //var maxWidth = 482.6, maxHeight = 269.1;
            var maxWidth = 158,
              maxHeight = 82;
            // Source width and height converted to mm (1px = 0.264583333mm)
            var srcWidth = slides[j].width * 0.264583333,
              srcHeight = slides[j].height * 0.264583333;
            // Resize asset while keeping original aspect ratio
            var scaled = calculateAspectRatioFit(srcWidth, srcHeight, maxWidth, maxHeight);
            // If the current asset is a PDF
            console.log(scaled.width, scaled.height);
            if (slides[j].extension == "pdf") {
              // Add the asset name to the top of the slide and show the generated thumbnail
              centeredText("(PDF) " + slides[j].assetname, 10);
              centeredImage(slides[j].base64, 'png', 20, scaled.width * 0.7, scaled.height * 0.7);
            } else {
              // Display the image asset (all image assets are converted to png in base64 conversion)
              centeredImage(slides[j].base64, 'png', 10, scaled.width, scaled.height);
            }
          } else if (slides[j].assettype == "link") {
            // Display the link in the center of the page
            doc.setTextColor(26, 13, 171);
            centeredText(slides[j].link, 50);
            doc.setTextColor(0, 0, 0);
          }
        }
        // Save the PDF
        doc.save(info.sessionName + ".pdf");
        // Wait 3 seconds then prompt user to download any asset PDF files
        setTimeout(function () {
          for (var i = 0; i < pdfs.length; i++) {
            downloadURI(pdfs[i].pdf, pdfs[i].assetname + ".pdf");
          }
        }, 3000);

      }
    };
    if (assets[i].asset.assettype == "file") {
      obj.extension = getFileExtension(assets[i].asset.assetLocation);
      if (obj.extension == "pdf") {
        obj.pdf = assets[i].asset.assetLocation;
        obj.src = assets[i].asset.thumbnailLocation;
      } else {
        obj.src = assets[i].asset.assetLocation;
      }
    } else if (assets[i].asset.assettype == "link") {
      // This source does not get used anywhere because the asset type is a link
      // Only needed to satisfy the obj.onload callback (its an image object storing extra info)
      obj.src = "https://i.imgur.com/ZVYirCC.png";
    }
  }
}

// https://stackoverflow.com/a/14731922
function calculateAspectRatioFit(srcWidth, srcHeight, maxWidth, maxHeight) {
  var ratio = Math.min(maxWidth / srcWidth, maxHeight / srcHeight);
  var scaled = {
    width: srcWidth * ratio,
    height: srcHeight * ratio
  }
  return scaled;
}

// Prompt the user to download a file from (uri) with the filename (name)
function downloadURI(uri, name) {
  var link = document.createElement("a");
  link.download = name;
  link.href = uri;
  link.click();
}

deleteButton.addEventListener("click", function () {
  if (window.confirm("Are you sure you want to delete this session?")) {
    $.ajax({
      type: "POST",
      url: "/sessions/" + sessionID + "/delete",
      timeout: 60000,
      success: function (data) {
        var retrieved = JSON.parse(data);
        if (retrieved['success'])
          window.location.replace("/sessions");
        else
          console.log("Could not delete the session id " + sessionID);
      }
    });
  } else {
    e.preventDefault();
  }
});


function applyGestureControls() {
  $('.assetThumbnail').each(function () {
    var element = $(this);
    // Make sure this method not applied to a thumbnail more than once
    if (element.hasClass("gestures-added")) {
      return true;
    } else {
      element.addClass("gestures-added");
    }

    // Add animation class if not already added (addClass checks first)
    element.addClass("animated");
    element.addClass("faster");
    var gestures = new Hammer(this, {
      touchAction: "pan-x"
    });

    // listen for a tap event...
    gestures.on("tap", function (ev) {
      // Load the image popup
      element.magnificPopup({
        items: {
          src: element.attr('src'),
          title: element.attr('title'),
          type: 'image'
        }
      });
    });
  });
}