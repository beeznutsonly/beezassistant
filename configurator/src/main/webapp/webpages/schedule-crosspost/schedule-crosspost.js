$(document).ready(
    function(){
        $("#scheduledCrosspostForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );
    }
);
function ajaxPost(){
    var formData = cureFormData({
        url : $("#url").val(),
        title : $("#title").val(),
        scheduledTime : getISODateTimeFromPicker("#scheduledTime", true),
        subreddit : $("#subreddit").val()
    });

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.protocol + "//" + window.location.host + "/api/scheduledcrossposts",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function() {                  
            submissionFeedbackAlert("Crosspost successfully scheduled", "success");
        },
        error: function(er) {
            submissionFeedbackAlert("Failed to schedule your crosspost: " + er, "danger");
        }
    });
}