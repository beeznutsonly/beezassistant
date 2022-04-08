const normalInputRegex = ".*[a-zA-Z0-9]+.*";

$(document).ready(function(){
    $(".list-group").each(function(){
        makeListGroupNavigable($(this));
    });
    $(".form-fields .form-control").each(function() {
        $(this).attr("pattern", normalInputRegex)
    })
    enableCustomValidation();
});

function isTextEmpty(text) {
    return $.trim(text) == "";
}

function enableCustomValidation() {
    'use strict'
  
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopImmediatePropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
}

function convertBlanksToNulls(dataObject) {
    const newDataObject = dataObject;
    Object.keys(newDataObject).forEach((key, index) => {
        if (isTextEmpty(newDataObject[key])) {
            newDataObject[key] = null;
        }
    })
    return newDataObject;
}

function cureFormData(dataObject) {
    const newDataObject = dataObject;
    Object.keys(newDataObject).forEach((key, index) => {
        newDataObject[key] = $.trim(newDataObject[key])
    })
    return convertBlanksToNulls(newDataObject);
}

function submissionFeedbackAlert(message, type) {
    var alertElement = $("<div>", {
        "class": "alert alert-" + type + " alert-dismissible",
        "role": "alert"
    });
    $(alertElement).append(
        message,
        $("<button>", {
            "type":"button", 
            "class":"btn-close", 
            "data-bs-dismiss":"alert", 
            "aria-label":"Close"
        })
    );
    $(".feedback-alert-card").html(alertElement);
}

function makeListGroupNavigable(listGroup) {
    $(listGroup).on("keydown", function(event) {
        if (event.key == "ArrowUp" || event.key == "ArrowDown") {
            const firstIndex = $(listGroup).find('.list-group-item').first().index();
            const lastIndex = $(listGroup).find('.list-group-item').last().index();
            var currentIndex;
            var newIndex;
            
            switch (event.key) {
                case "ArrowUp":
                    currentIndex = $(listGroup).find(".active").first().index();
                    newIndex = (currentIndex == firstIndex ? firstIndex : currentIndex - 1);
                    break;
                case "ArrowDown":
                    currentIndex = $(listGroup).find(".active").last().index();
                    newIndex = (currentIndex == lastIndex ? lastIndex : currentIndex + 1);
                    break;
            }
            
            if (!event.shiftKey) {
                $(listGroup).find('.active').removeClass('active');
            }
            $(listGroup).find('.list-group-item:eq( '+ newIndex +' )').addClass('active');
        }
        else if (event.key.toLowerCase() == "a" && event.ctrlKey) {
            event.preventDefault();
            $(listGroup).find('.list-group-item').addClass('active');
        }
    })
}

function addToListGroup(listGroupElement, listGroupItemContent, dataObject) {
    var listItem = $("<a>", {
        "href": "#", 
        "class": "list-group-item list-group-item-action"
    });
    $(listItem).on("click", function(event) {
        if (event.ctrlKey) {
            event.preventDefault();
            if ($(this).hasClass("active")) {
                $(this).removeClass("active");
            }
            else {
                $(this).addClass("active");
            }
        }
        else {
            $(".list-group .list-group-item").removeClass("active");
            $(this).addClass("active");
        }
    });
    $(listItem).append(listGroupItemContent);
    $(listGroupElement).append(listItem);
    $(listItem).data(dataObject)
}