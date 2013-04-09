$(function () {

    $('#id_language').on('change', function () {
        var lang = $('#id_language').val();
        var uri = URI(document.location);
        uri.removeSearch('lang');
        uri.addSearch('lang', lang);
        document.location = uri.href();
    });


});