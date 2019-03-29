var sessionNameInput = document.getElementById("sessionNameInput");
var saveButton = document.getElementById("session-save");
var deleteButton = document.getElementById("session-delete");
var sessionID = parseInt($(".session-page").attr("id"));

// function that updates the thumbnail if it is the name of the assets and
// when it has been updated
sessionNameInput.addEventListener('change', function(){
    // checks if the "use name as thumbnail" checkbox has been ticked before
    // updating the thumbnail
    var name = sessionNameInput.value;
  });

saveButton.addEventListener("click", function(){
    document.getElementById("formUpdate").submit();
})

deleteButton.addEventListener("click", function(){
    if(window.confirm("Are you sure you want to delete this session?"))
    {
        $.ajax({
            type: "POST",
            url: "/sessions/" + sessionID + "/delete",
            timeout: 60000,
            success: function (data) {
                var retrieved = JSON.parse(data);
                if(retrieved['success'])
                    window.location.replace("/sessions");
                else
                    console.log("Could not delete the session id " + sessionID);
            }
        });
    }
    else
    {
        e.preventDefault();
    }
});