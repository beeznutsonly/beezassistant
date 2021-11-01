$(document).ready(
    function(){
        $("#adminUpdateForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );

        function ajaxPost(){
            var formData = {
                heading : $("#heading").val() == '' ? null : $("#heading").val(),
                details : $("#details").val() == '' ? null : $("#details").val(),
            }

            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: window.location.protocol + "//" + window.location.host + "/adminupdates",
                data: JSON.stringify(formData),
                dataType: "json",
                success: function(){
                    alert("Admin update successfully added");
                },
                error: function(error){
                    alert("Failed to add admin update: " + JSON.stringify(error))
                }
            })
        }
    }
)