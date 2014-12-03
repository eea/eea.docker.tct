$(function () {
   $('.change-lang').on('click', function () {
        $(this).parent().find('form').submit();
   });

   var indicator_modal = $('#indicator_modal');
   indicator_modal.on('hidden', function () {
     indicator_modal.data('modal', false);
     indicator_modal.html('');
   });

});
