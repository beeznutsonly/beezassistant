// Requires jQuery, moment.js, and jQuery datetimepicker

$.datetimepicker.setDateFormatter({
    parseDate: function (date, format) {
        var d = moment(date, format);
        return d.isValid() ? d.toDate() : false;
    },
    formatDate: function (date, format) {
        return moment(date).format(format);
    }
});

$(".datetimepicker").datetimepicker({
    format: 'dddd, DD MMM YYYY HH:mm',
    formatDate: 'YYYY-MM-DD',
    formatTime: 'HH:mm',
    minDate: 0
});

$('.datepicker').datetimepicker({
    format: 'dddd, DD MMM YYYY',
    formatDate: 'YYYY-MM-DD',
    timepicker: false
});

function getISODateTimeFromPicker(picker, timezone) {
    dateTime = $(picker).datetimepicker('getValue');
    format = timezone ? 'YYYY-MM-DDTHH:mm:00Z' : 'YYYY-MM-DDTHH:mm:00';
    return moment(dateTime).format(format);
}

function getISODateFromPicker(picker){
    dateTime = $(picker).datetimepicker('getValue');
    return moment(dateTime).format(
        moment.HTML5_FMT.DATE
    );
}