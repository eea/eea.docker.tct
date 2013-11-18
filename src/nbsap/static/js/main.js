$(function () {
   $('.change-lang').on('click', function (e) {
        e.preventDefault()
        $(this).parents('form').submit();
   });
});
