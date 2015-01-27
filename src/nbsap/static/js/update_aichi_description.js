$(function(){
  update_description();
  function update_description(){
    var ids = $("#id_aichi_targets").val();
    var descr = $('#descriptions');
    $.ajax({
      url: descr.data('url'),
      data: "targets="+ids,
      success: function(data) {
        descr.empty();
        $.each(data, function (index, element) {
          descr.append(
            $("<li><b>"+element[0]+"</b>: "+ element[1]+"</li>")
          );
        });
      }
    });
  }

  $("#id_aichi_targets").change(update_description);
});
