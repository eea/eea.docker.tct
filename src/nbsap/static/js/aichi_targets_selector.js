$(function() {
  $(".chzn-select").chosen();
  $('select[name=aichi_targets]').on('change', function () {
    var option = $(this).serialize();
    var text = $(this).parents('.form-group').find('.aichi_targets_text');
    var args = option.split("aichi_targets=");
    args = args.map(function(x) {return parseInt(x)});
    args = args.filter(Number);
    var url = text.data('url');
    text.html('');
    $.each(args, function(i, arg) {
      $.get(url.replace('1',arg), function(data) {
      data = $.parseJSON(data)[0];
      text.append('<h5>Target ' + data.code + '</h5><p>' + data.value + '</p>');
      });
    });
  }).change();
});
