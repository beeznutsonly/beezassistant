$(document).ready(
    function(){
        refreshScheduledSubmissions();
    }
);
function refreshScheduledSubmissions(){
    $.ajax({
        url: window.location.protocol + "//" + window.location.host + "/api/scheduledsubmissions",
        success: function(result){
            var scheduledSubmissionsView = Metro.getPlugin("#scheduledSubmissionsListView", "listview");
            scheduledSubmissions = result._embedded.scheduledSubmissions;

            for (const scheduledSubmission of scheduledSubmissions){
                var listViewItem = scheduledSubmissionsView.add(null, scheduledSubmission);
                $(listViewItem).data(scheduledSubmission);
            }
        },
        dataType: "json"
    });
}
function deleteScheduledSubmission(){
    var scheduledSubmissionsView = Metro.getPlugin("#scheduledSubmissionsListView", "listview");
    selectedNode = $(".node.current.current-select");
    scheduledSubmission = $(selectedNode).data();
    if (confirm("Are you sure you want to delete the selected scheduled submission?")){
        scheduledSubmissionURL = scheduledSubmission._links.scheduledSubmission.href;
        $.ajax({
            type: "DELETE",
            url: scheduledSubmissionURL,
            success: function(){
                scheduledSubmissionsView.del(selectedNode);
                alert("Scheduled submission deleted")
            },
            error: function(error){
                alert("Could not delete the scheduled submission: " + JSON.stringify(error));
            },
            dataType: "json"
        });
    }
}

function scheduleSubmission(){
    window.open("schedulesubmission");
}
function onNodeClick(){
    $("#btnRemoveSubmission").removeAttr("disabled");
}