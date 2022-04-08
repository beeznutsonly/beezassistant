$(document).ready(
    function(){
        $("#scheduledSubmissionForm").submit(
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
        scheduledTime : getISODateTimeFromPicker(
            "#scheduledTime", 
            true
        ),
        flairId : $("#flairId").val(),
        subreddit : $("#subreddit").val(),
        commentBody : $("#commentBody").val()
    });
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.protocol + "//" + window.location.host + "/scheduledsubmissions",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function() {
            if (!isTextEmpty(formData.commentBody)) {
                var autoReply = {
                    url: formData.url,
                    subreddit: formData.subreddit,
                    commentBody: formData.commentBody
                }
                $.ajax({
                    type: "POST",
                    contentType: "application/json",
                    url: window.location.protocol + "//" + window.location.host + "/scheduledsubmissionautoreplies",
                    data: JSON.stringify(autoReply),
                    dataType: "json",
                    error: function(er) {
                        alert("Failed register your autoreply: " + er);
                    }
                });
            }                   
            submissionFeedbackAlert("Submission successfully scheduled", "success");
        },
        error: function(er) {
            submissionFeedbackAlert("Failed to schedule your submission: " + er, "danger");
        }
    })
}