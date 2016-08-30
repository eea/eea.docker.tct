$(".delete").on("submit", function (e) {
  var message = $(this).find(".edit").data("message");
  e.preventDefault();
  if(confirm(message)){
    this.submit();
  }
});
