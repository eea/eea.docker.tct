$(".delete").on("submit", function (e) {
  var message = $(".edit").data("message");
  e.preventDefault();
  if(confirm(message)){
    this.submit();
  }
});
