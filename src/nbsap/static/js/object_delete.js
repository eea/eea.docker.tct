$(function () {
  $('.messages').delay(1000).fadeOut();
});

$("form").on("submit", function (e) {
  var message = $("button.btn-danger").data("message");
  e.preventDefault();
  if(confirm(message)){
    this.submit();
  }
});
