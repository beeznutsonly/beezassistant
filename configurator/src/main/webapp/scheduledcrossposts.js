$(document).ready(
    function(){
        refreshScheduledSubmissions();
    }
)
function refreshScheduledSubmissions(){
    $.ajax({
        url: window.location.protocol + "//" + window.location.host + "/scheduledcrossposts",
        success: function(result){
            var scheduledCrosspostsView = Metro.getPlugin("#scheduledCrosspostsListView", "listview");
            scheduledCrossposts = result._embedded.scheduledCrossposts;

            for (const scheduledCrosspost of scheduledCrossposts){
                var listViewItem = scheduledCrosspostsView.add(null, scheduledCrosspost);
                $(listViewItem).data(scheduledCrosspost);
            }
        },
        dataType: "json"
    });
}
function deleteScheduledCrosspost(){
    var scheduledCrosspostsView = Metro.getPlugin("#scheduledCrosspostsListView", "listview");
    selectedNode = $(".node.current.current-select");
    scheduledCrosspost = $(selectedNode).data();
    if (confirm("Are you sure you want to delete the selected scheduled crosspost?")){
        scheduledCrosspostURL = scheduledCrosspost._links.scheduledCrosspost.href;
        $.ajax({
            type: "DELETE",
            url: scheduledCrosspostURL,
            success: function(){
                scheduledCrosspostsView.del(selectedNode);
                alert("Scheduled crosspost deleted")
            },
            error: function(error){
                alert("Could not delete the scheduled crosspost: " + JSON.stringify(error));
            },
            dataType: "json"
        });
    }
}
function onNodeClick(){
    $("#btnRemoveCrosspost").removeAttr("disabled");
}