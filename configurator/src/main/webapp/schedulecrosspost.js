$(document).ready(
    function(){
        $("#scheduledCrosspostForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );
        function ajaxPost(){
            var formData = {
                url : $("#url").val(),
                title : $("#title").val(),
                scheduledTime : getISODateTimeFromPicker("#scheduledTime", true),
                subreddit : $("#subreddit").val()
            }

            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: window.location.protocol + "//" + window.location.host + "/scheduledcrossposts",
                data: JSON.stringify(formData),
                dataType: "json",
                success: function() {                  
                    alert("Crosspost successfully scheduled");
                },
                error: function(er) {
                    alert("Failed to schedule your crosspost: " + er);
                }
            })
        }
    }
)