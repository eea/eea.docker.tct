$(".delete").on("submit", function (e) {
  var message = $("form > button.btn-danger").data("message");
  e.preventDefault();
  if(confirm(message)){
    this.submit();
  }
});
