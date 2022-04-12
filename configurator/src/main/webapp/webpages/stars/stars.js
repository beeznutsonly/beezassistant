$(document).ready(
    function(){
        refreshStars();
    }
)
function refreshStars(){
    $.ajax({
        url: window.location.protocol + "//" + window.location.host + "/api/stars",
        success: function(result){
            var starsView = Metro.getPlugin("#starsListView", "listview");
            stars = result._embedded.stars;

            for (const star of stars){
                var listViewItem = starsView.add(null, star);
                $(listViewItem).data(star);
            }
        },
        dataType: "json"
    });
}
function deleteStar(){
    var starsView = Metro.getPlugin("#starsListView", "listview");
    selectedNode = $(".node.current.current-select");
    star = $(selectedNode).data();
    if (confirm("Are you sure you want to delete the selected star?")){
        starURL = star._links.star.href;
        $.ajax({
            type: "DELETE",
            url: starURL,
            success: function(){
                starsView.del(selectedNode);
                alert("Star deleted")
            },
            error: function(error){
                alert("Could not delete the star: " + JSON.stringify(error));
            },
            dataType: "json"
        });
    }
}
function onNodeClick(){
    $("#btnRemoveStar").removeAttr("disabled");
}

function addstar(){
    window.open("addstar");
}