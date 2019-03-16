var deleteButton = document.getElementById("session-delete");
var sessionID = parseInt($(".session").attr("id"));
console.log(sessionID);
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