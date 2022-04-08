$(document).ready(
    function() {
        $("#name").on(
            "input",
            determineAddStarLinkButtonStatus
        )
        $("#linkName").on(
            "input",
            determineAddStarLinkButtonStatus
        )
        $("#link").on(
            "input",
            determineAddStarLinkButtonStatus
        )
        $("#btnAddStarLink").click(
            addStarLink
        )
        $("#btnRemoveStarLink").click(
            removeStarLink
        )
        $("#star-form").submit(
            function(event){
                event.preventDefault();
                ajaxPost();
            }
        );
    }
);

function determineAddStarLinkButtonStatus() {
    if (checkStarLinkFormData()) {
        $("#btnAddStarLink").removeAttr("disabled");
    }
    else {
        $("#btnAddStarLink").attr("disabled", "true");
    }
}

function checkStarLinkFormData() {
    return !(
        isTextEmpty($("#name").val()) || 
        isTextEmpty($("#linkName").val()) || 
        isTextEmpty($("#link").val())
    );
}

function addStarLink() {
    var starLink = {
        name : $("#name").val(),
        linkName : $("#linkName").val(),
        link : $("#link").val()
    };
    var linkNameLabel = $("<label>", {"class": "star-link-label"});
    var linkLabel = $("<label>", {"class": "star-link-label"});
    var listItemContent = $("<div>", {"class": "list-group-item-content"});
    
    $(linkNameLabel).append(starLink.linkName);
    $(linkLabel).append(starLink.link);
    $(listItemContent).append(linkNameLabel, linkLabel);
    addToListGroup($("#star-links-list-group"), listItemContent, starLink);
}

function removeStarLink() {
    $(".list-group-item.active").remove();
}

function ajaxPost(){
    var formData = cureFormData({
        name : $("#name").val(),
        birthday : getISODateFromPicker("#birthday"),
        nationality : $("#nationality").val(),
        birthPlace : $("#birthPlace").val(),
        yearsActive : $("#yearsActive").val(),
        description : $("#description").val()
    });

    $.ajax({
        type: "POST",
        contentType: "application/json",
        url: window.location.protocol + "//" + window.location.host + "/stars",
        data: JSON.stringify(formData),
        dataType: "json",
        success: function(){
            submissionFeedbackAlert("Star info successfully added", "success");
            const starLinks = [];
            $('.list-group-item').each(function(){
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
                        submissionFeedbackAlert(
                            "Failed to register starlink: " + 
                            JSON.stringify(error),
                            "danger"
                        );
                    }
                })
            }
        },
        error: function(error){
            submissionFeedbackAlert(
                "Failed to add star info: " + error, 
                "danger"
            )
        }
    });
}