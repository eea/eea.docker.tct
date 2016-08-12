$(".chzn-select").chosen();
$(function () {
  $('select[name=aichi_goals]').on('change', function () {
    var option = $(this).val();
    var text = $(this).parents('.form-group').find('.goal_text');
    if (option == null){
      $(this).val = '';
      text.html('');
    } else {
      var urls = [];
      $.each(option, function(i, op){
        url = "{% url 'goal_title' pk=1%}".replace('1', op);
        urls.push(url);
      });

      $.each(urls, function(i, url){
        text.html('');
        $.get(url, function (data) {
          data = $.parseJSON(data)[0];
          text.append('<h5>Goal ' + data.code.toUpperCase() + '</h5>');
          text.append('<p>' + data.goal + '</p>');
          $('select[name=aichi_targets]').html('');
          $.each(data.targets, function(i,t) {
            var html = $('<option />').attr('value', t.pk).text('Target ' + t.value);
            $('select[name=aichi_targets]').append(html);
          });
          $('select[name=aichi_targets]').change();
          $('select[name=aichi_targets]').trigger("chosen:updated");
        })
      });
    }
  }).change();
});
