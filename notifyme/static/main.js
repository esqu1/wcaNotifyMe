$(document).ready(function () {
  var closeButtonStr = '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
  $('#message').hide();
  $("#submitForm").submit(function (e) {
    $.ajax({
      type: "POST",
      url: '/submitted',
      data: {
        email: $('#email').val(),
        comp_name: $('#compname').val()
      },
      success: function (data) {
        if ('error' in data) {
          $('#alertContainer').html('<div role="alert" id="message" class="alert alert-danger alert-dismissible fade show">' + data.error + closeButtonStr + '</div>');
        } else {
          $('#alertContainer').html('<div role="alert" id="message" class="alert alert-success alert-dismissible fade show">' + 'Success! You will be notified when registration opens.' + closeButtonStr + '</div>');
        }
      }
    });
    e.preventDefault();
  });
})