$(document).ready(
    function(){
        $("#starForm").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );


        function ajaxPost(){
            var formData = {
                name : $("#name").val(),
                birthday : getISODateFromPicker("#birthday"),
                nationality : $("#nationality").val(),
                birthPlace : $("#birthPlace").val(),
                yearsActive : $("#yearsActive").val(),
                description : $("#description").val()
            }

            $.ajax({
                type: "POST",
                contentType: "application/json",
                url: window.location.protocol + "//" + window.location.host + "/stars",
                data: JSON.stringify(formData),
                dataType: "json",
                success: function(){
                    alert("Star info successfully added");
                },
                error: function(error){
                    alert("Failed to add star info: " + error)
                }
            })
        }
    }
)

