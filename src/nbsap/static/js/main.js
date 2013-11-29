$(function () {
   $('.change-lang').on('click', function () {
        $(this).parent().find('form').submit();
   });
});
