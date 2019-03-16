var currentResults = document.getElementById("currentRow");
var frequentResults = document.getElementById("frequentRow");
var storageBool = storageAvailable('localStorage');
// Get the assets from the active session
var assets = fetch_active_session_assets();
assets = assets.assets;
console.log(assets);
var noSleep = new NoSleep();
var socket;
$(document).ready(function () {
  socket = io();
});
var selectedTab = '1';
var maxTabs = 5;

var listening;
var microphoneToggle = document.getElementById("microphoneToggle");
var microphoneIcon = document.getElementById("microphoneIcon");

setupPage();

//################# ANNYANG START ########################

if (annyang) {
  var recognisedTags = []; // will store recognised tags so they can be removed from the next result
  // the list is cleared when there is a gap in speech
  // the tags will be pulled from the server
  var recognisedTagsUsed = [];
  var tagset = fetchTagset();

  annyang.addCallback('result', function (phrases) {
    var text = phrases[0];
    text = text.toLowerCase();

    // checking if the list is not empty before iterating through it!
    if (recognisedTagsUsed.length != 0) {
      recognisedTagsUsed.forEach(function (item) {
        text = text.replace(item, "");
      });
    }
    // prints the result with recognised tags removed
    console.log("Recognized text: ", text);
    // goes through the tags and checks if they are in the text
    tagset.forEach(function (tag) {
      if (text.toLowerCase().includes(tag)) {
        // adds the new recognised tag into the recognisedTag list
        recognisedTags.push(tag);
        console.log(recognisedTags);
        text.replace(tag, "");
      }
    });

    // this will also empty what's currently in the recognised tags
    if (recognisedTags) {
      makeAjaxRequest();
      recognisedTagsUsed = recognisedTagsUsed.concat(recognisedTags);
      recognisedTags = [];
    }

  });

  annyang.addCallback('end', function () {
    if (recognisedTagsUsed.length != 0) {
      recognisedTagsUsed = [];
    }
  });
  // Start listening. You can call this here, or attach this call to an event, button, etc.

  microphoneToggle.addEventListener('click', function () {
    if (listening) {
      stopListening();
    } else {
      startListening();
    }
  });
}

function startListening() {
  noSleep.enable();
  annyang.start({
    autoRestart: true,
    continuous: false
  });
  var recognition = annyang.getSpeechRecognizer();
  recognition.interimResults = true;
  console.log("Started listening");

  microphoneIcon.classList.add("fa-microphone");
  microphoneIcon.classList.remove("fa-microphone-slash");
  listening = true;
}

function stopListening() {
  if (listening) {
    console.log("Stopped listening");
  }
  noSleep.disable();
  annyang.abort()
  microphoneIcon.classList.add("fa-microphone-slash");
  microphoneIcon.classList.remove("fa-microphone");
  listening = false;
}

function setupPage() {
  localStorage.clear();
  loadAssetsFromSession();
  stopListening();

  if (!localStorage.getItem('tabs')) {
    localStorage.setItem('tabs', '{}');
    addTab();
  } else {
    renderTabs();
  }

  document.getElementById('addTabBtn').addEventListener(
    'click',
    function () {
      addTab();
    });
  populateActiveTab();

  var items = JSON.parse(localStorage.getItem("lastAssets"));
  if (items) {
    updateResults(items);
  }
}

function makeAjaxRequest() {
  //only works if local storage is a available in the browser
  if (storageBool) {
    console.log("localStorage available");

    var mentionedTags = localStorage.getItem('mentionedTags');
    if (mentionedTags) {
      $.ajax({
        type: "POST",
        url: "/compare_phrases",
        data: {
          'recognisedTags': JSON.stringify(recognisedTags),
          'mentionedTags': mentionedTags
        },
        timeout: 60000,
        success: function (data) {
          var retrieved = JSON.parse(data);
          console.log(retrieved);
          updateResults(retrieved['assetResults']);
          localStorage.setItem('mentionedTags', JSON.stringify(retrieved[
            'mentionedTags']));
          localStorage.setItem('lastAssets', JSON.stringify(retrieved[
            'assetResults']));
        }
      });
    } else {
      $.ajax({
        type: "POST",
        url: "/compare_phrases",
        data: {
          'recognisedTags': JSON.stringify(recognisedTags),
        },
        timeout: 60000,
        success: function (data) {
          var retrieved = JSON.parse(data);
          console.log(retrieved);
          updateResults(retrieved['assetResults']);
          localStorage.setItem('mentionedTags', JSON.stringify(retrieved[
            'mentionedTags']));
          localStorage.setItem('lastAssets', JSON.stringify(retrieved[
            'assetResults']));
        }
      });
    }
  }
}

function updateResults(assets) {
  frequentResults.innerHTML = "";
  for (asset in assets['frequent']) {
    var image = document.createElement("IMG");
    var thumbnail = assets['frequent'][asset]['thumbnailLocation'];
    if (thumbnail != null) {
      image.src = thumbnail;
    } else {
      image.src = "https://i.imgur.com/5NqcCVN.png";
    }
    image.setAttribute("data-id", assets['frequent'][asset]['id']);
    image.setAttribute("title", assets['frequent'][asset]['asset']);
    image.classList.add("assetThumbnail");
    image.classList.add("animated");
    image.classList.add("faster");
    frequentResults.appendChild(image);
  }
  currentResults.innerHTML = "";
  for (asset in assets['current']) {
    var image = document.createElement("IMG");
    var thumbnail = assets['current'][asset]['thumbnailLocation'];
    if (thumbnail != null) {
      image.src = thumbnail;
    } else {
      image.src = "https://i.imgur.com/5NqcCVN.png";
    }
    image.setAttribute("data-id", assets['current'][asset]['id']);
    image.setAttribute("title", assets['current'][asset]['asset']);
    image.classList.add("assetThumbnail");
    image.classList.add("animated");
    image.classList.add("faster");
    currentResults.appendChild(image);
  }
  applyGestureControls();
}

// TABS LOGIC
function addTab() {
  //add tab to localstorage
  var tabs = JSON.parse(localStorage.getItem('tabs'));
  var totalTabs = Object.keys(tabs).length
  if (totalTabs < maxTabs) {
    var numOfTab = totalTabs + 1;
    tabs[numOfTab] = [];
    localStorage.setItem('tabs', JSON.stringify(tabs));
    renderTabs();
  } else {
    console.log("Maximum number of tabs opened");
  }
}

function renderTabs() {
  var tabs = JSON.parse(localStorage.getItem('tabs'));
  var tabPanel = document.getElementById("tabPanel");
  tabPanel.innerHTML = "";
  var keys = Object.keys(tabs);
  keys.forEach(function (key) {
    var tabDiv = document.createElement("DIV");
    tabDiv.classList.add("whiteText");
    tabDiv.classList.add("bubbleButton");
    tabDiv.classList.add("bubbleButtonDark");
    tabDiv.classList.add("rowsButton");
    if (selectedTab == key) {
      tabDiv.classList.add("selected");
    }
    tabDiv.innerHTML = "Tab " + key;

    tabDiv.addEventListener("click", function () {
      selectedTab = key.toString();
      renderTabs();
      populateActiveTab();
    });

    tabPanel.append(tabDiv);
  });
}

function addToCurrentTab(assetID) {
  var tabs = JSON.parse(localStorage.getItem('tabs'));
  var asset = getAsset(assetID);
  tabs[selectedTab].push(asset);
  localStorage.setItem('tabs', JSON.stringify(tabs));
  populateActiveTab();
}

function loadAssetsFromSession()
{
  var maxTab = 0;
  
  var tabs = {}
  // Find the maximum tab
  for (var i = 0; i < assets.length; i++)
  {
    if (maxTab < assets[i].tab)
    {
      maxTab = assets[i].tab;
    }
  }
  // Initialise all the tabs
  for (var i = 1; i <= maxTab; i++)
  {
    tabs[i] = [];
  }
  // Add the asset to the relevant tab
  for (var i = 0; i < assets.length; i++)
  {
    var currentTab = assets[i].tab;
    tabs[currentTab].push(assets[i].asset);
  }
  localStorage.setItem('tabs', JSON.stringify(tabs));
  populateActiveTab();
}

function fetch_active_session_assets() {
  var tmp = null;
  $.ajax({
    async: false,
    url: "/fetch_active_session_assets",
    timeout: 60000,
    success: function (data) {
      tmp = data;
    }
  });
  return tmp;
}

function getAsset(assetID) {
  var tmp = null;
  $.ajax({
    async: false,
    url: "/fetch_asset",
    data: {
      'id': assetID
    },
    timeout: 60000,
    success: function (data) {
      tmp = JSON.parse(data);
    }
  });
  return tmp;
}

function populateActiveTab() {
  var tabRow = document.getElementById("currentTabRow");
  assets = JSON.parse(localStorage.getItem('tabs'))[selectedTab];
  tabRow.innerHTML = "";
  for (asset in assets) {
    var image = document.createElement("IMG");
    var thumbnail = assets[asset]['thumbnailLocation'];
    if (thumbnail != null) {
      image.src = thumbnail;
    } else {
      image.src = "https://i.imgur.com/5NqcCVN.png";
    }
    image.setAttribute("data-id", assets[asset]['id']);
    image.setAttribute("title", assets[asset]['asset']);
    image.classList.add("assetThumbnail");
    image.classList.add("animated");
    image.classList.add("faster");
    // this adds the new thing to the start of tab as opposed to append at end
    tabRow.insertBefore(image, tabRow.children[0]);
  }
  applyGestureControls();

}
// END OF TABS LOGIC

function storageAvailable(type) {
  try {
    var storage = window[type];
    var x = '_storage_test__';
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    return e instanceof DOMException && (
        e.code === 22 ||
        e.code === 1014 ||
        e.name === 'QuotaExceededError' ||
        e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
      storage.length !== 0;
  }
}

function flushRecentTags() {
  storedTags = JSON.parse(localStorage.getItem('mentionedTags'));
  if (storedTags != null)
  {
    console.log(storedTags);
    storedTags['recent'] = {};
    localStorage.setItem('mentionedTags', JSON.stringify(storedTags));
  }
}

function fetchTagset() {
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
        },
        callbacks: {
          open: function () {
            $('.mfp-img').each(function () {
              var popupImage = $(this);
              // Make sure this method not applied to a thumbnail more than once
              if (popupImage.hasClass("gestures-added")) {
                return true;
              } else {
                popupImage.addClass("gestures-added");
                popupImage.addClass("animated");
                popupImage.addClass("faster");
              }
              var popupGestures = new Hammer(this, {
                touchAction: "pan-x"
              });
              // enable swipe detection for all directions
              popupGestures.get('swipe').set({
                direction: Hammer.DIRECTION_ALL,
                threshold: 1,
                velocity: 0.1
              });

              // listen to events...
              popupGestures.on("swipeup", function (ev) {
                // Swipe up gesture
                if (ev.type == "swipeup") {
                  popupImage.addClass("slideOutUp");
                  var assetID = element.attr('data-id');
                  var data = {
                    id: assetID,
                    tab: selectedTab
                  }
                  socket.emit('event', data);
                  addToCurrentTab(assetID);
                  flushRecentTags();
                  console.log("sent ID " + assetID + " to socketIO");
                  setTimeout(function () {
                    var magnificPopup = $.magnificPopup.instance;
                    magnificPopup.close();
                  }, 500);
                }
              });
            });
          },
        }
      });
    });
  });
}

// Prevent chrome popup menu on hold (android)
var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1; //&& ua.indexOf("mobile");
if (isAndroid) {
  window.oncontextmenu = function (event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
  };
}
