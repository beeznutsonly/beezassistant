jQuery('.datetimepicker').datetimepicker({
    format: "c",
    showTimezone: true
});
$(document).ready(
    function(){
        $("#scheduledSubmissionForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );

        function ajaxPost(){
            var formData = {
                url : $("#url").val(),
                title : $("#title").val(),
                scheduledTime : $("#scheduledTime").val(),
                flairId : $("#flairId").val(),
                subreddit : $("#subreddit").val(),
                commentBody : $("#commentBody").val()
            }

            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: window.location.protocol + "//" + window.location.host + "/scheduledsubmissions",
                data: JSON.stringify(formData),
                dataType: "json",
                success: function() {
                    if (formData.commentBody && !(formData.commentBody.trim() === "")){
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
                    alert("Submission successfully scheduled");
                },
                error: function(er) {
                    alert("Failed to schedule your submission: " + er);
                }
            })
        }
    }
)