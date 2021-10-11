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
                    const starLinks = [];
                    $('.node').each(function(){
                        starLinks.push($(this).data())
                    });
                    for (const starLink of starLinks){
                        $.ajax({
                            type: "POST",
                            contentType: "application/json",
                            url: window.location.protocol + "//" + window.location.host + "/starlinks",
                            data: JSON.stringify(starLink),
                            dataType: "json",
                            error: function(error){
                                alert("Failed to register starlink: " + JSON.stringify(error));
                            }
                        })
                    }
                },
                error: function(error){
                    alert("Failed to add star info: " + error)
                }
            })
        }
    }
)
function addStarLink(){
    var starLink = {
        name : $("#name").val(),
        linkName : $("#linkName").val(),
        link : $("#link").val()
    };
    var starLinksListView = Metro.getPlugin("#starLinksListView", "listview");
    var listViewItem = starLinksListView.add(null, starLink);
    $(listViewItem).data(starLink);
}

function removeStarLink(){
    var starLinksListView = Metro.getPlugin("#starLinksListView", "listview");
    selectedNode = $(".node.current.current-select");
    starLinksListView.del(selectedNode);
}

function onNodeClick(){
    $("#btnRemoveStarLink").removeAttr("disabled");
}