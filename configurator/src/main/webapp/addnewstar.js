// Post Request
// -----------------------

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
                birthday : $("#birthday").val(),
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
                dataType: "json"
            })
        }
    }
)

