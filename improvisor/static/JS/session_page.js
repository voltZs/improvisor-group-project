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

function exportSlides(info, assets) {
  var doc = new jsPDF({
    orientation: 'landscape',
    format: 'a3'
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
  // Display the session name and session author (first name + lastname)
  centeredText(info.sessionName, 100);
  doc.setFontSize(20);
  centeredText(info.sessionAuthor, 115);
  var slides = [];

  for (var i = 0; i < assets.length; i++) {
    // Store the asset details in the image object (even if it is a link instead of a file)
    var obj = new Image();
    obj.id = assets[i].asset_id;
    obj.assettype = assets[i].asset.assettype;
    obj.link = assets[i].asset.assetLink;
    obj.date = assets[i].dateAdded
    obj.crossOrigin = "Anonymous";
    // Callback for when the source has loaded (obj.src = x)
    obj.onload = function () {
      if (this.assettype == "file") {
        slides.push({
          src: this.src,
          asset_id: this.id,
          assettype: this.assettype,
          link: this.link,
          dateAdded: this.date,
          base64: convertImgToBase64(this),
          width: this.width,
          height: this.height
        });
      }
      else if (this.assettype == "link") {
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
            doc.addImage(slides[j].base64, 'png', 45, 45, 150, 100);
          } else if (slides[j].assettype == "link") {
            doc.setTextColor(26, 13, 171);
            centeredText(slides[j].link, 100);
            doc.setTextColor(0, 0, 0);
          }
        }
        // Save the PDF
        doc.save('output.pdf');
      }
    };
    if (assets[i].asset.assettype == "file") {
      obj.src = assets[i].asset.assetLocation;
    }
    else if (assets[i].asset.assettype == "link")
    {
      // This source does not get used anywhere because the asset type is a link
      // Only needed to satisfy the obj.onload callback (its an image object storing extra info)
      obj.src = "https://i.imgur.com/ZVYirCC.png";
    }
  }
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