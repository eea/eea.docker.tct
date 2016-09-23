(function($) {
  $.ajaxSetup({
    beforeSend: function() {
      $('.loader-container').show();
    },
    complete: function() {
      $('.loader-container').hide();
    },
    success: function() {
      $('.loader-container').hide();
    }
  });
  $.ajaxGet = function(options) {
    var settings = $.extend({
      form: ".form",
      button: ".ajaxget"
    }, options);

    $(settings.button).on('click', function() {
      var url = $(this).data('url');
      $(settings.form).empty();
      $.get(url, function(data) {
        $(settings.form)
          .append(data)
          .find('form')
          .attr('action', url);
      })
      $('html, body').animate({
        scrollTop: $(settings.form).offset().top
      }, 800);
    });
  }

})(jQuery);
