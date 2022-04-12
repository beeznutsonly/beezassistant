$(document).ready(
    function(){
        $("#adminUpdateForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );
    }
);

function ajaxPost(){
    var formData = cureFormData({
        heading : $("#heading").val(),
        details : $("#details").val()
    });

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.protocol + "//" + window.location.host + "/api/adminupdates",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function(){
            submissionFeedbackAlert("Admin update successfully added", "success");
        },
        error: function(error){
            submissionFeedbackAlert("Failed to add admin update: " + JSON.stringify(error), "danger")
        }
    })
};