$(function () {

    $('#id_language').on('change', function () {
        var lang = $('#id_language').val();
        var form = $('form[name=set_lang_' + lang + ']');
        form.submit();
    });


});
