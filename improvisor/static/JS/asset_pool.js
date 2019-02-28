function getAssets(tags, sorting, limit){
    $.ajax({
      type: "POST",
      url: "/assets/select",
      data: {
        'filterTags': JSON.stringify(tags),
        'sorting': sorting,
        'limit': limit
      },
      timeout: 60000,
      success: function (data) {
        console.log(data)
      }
    });
}
