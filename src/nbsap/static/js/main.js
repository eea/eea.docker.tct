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

function Modal(container) {
    self = this;
    self.container = container;
    self.activeModal = null;

    self.open = function(target) {
        $(self).trigger({
          'type': 'modalopen',
          'target': target
        })
        self.activeModal = target;
        $(target).addClass('active');
        $('body').addClass('modal-open');
    };

    self.close = function() {
        target = self.activeModal;
        self.activeModal = null;
        $(target).removeClass('active');
        $('body').removeClass('modal-open');
    };

    // events - buttons
    $('[data-modal]').on('click', function(e) {
        e.preventDefault();
        target = $(this).data('modal');
        if (target == 'close') {
            self.close();
        } else {
          href = $(this).attr('href');
          if (href) {
            $.ajax({
              url: href,
              context: document.body,
              beforeSend: function() {
                $(target).html('loading');
              }
            }).done(function(html) {
              $(target).html(html);
            });
          }
          self.open(target);
        }
    });
    // events - close
    $(self.activeModal).on('click', function(event) {
        event.stopPropagation();
    });
    $(self.container).on('click', function() {
        if (self.activeModal) {
            self.close();
        }
    });
    $(document).keyup(function(e) {
        if (e.keyCode == 27 && self.activeModal) {
            self.close();
        }
    });
    $('.toc ul').columnlist({
        size : 4,
        'class' : 'column-list',
        incrementClass : 'column-list-'
    });
}

$(document).ready(function() {
  modal = new Modal($('.modal-container')[0]);
});

$(function () {
  $('.messages').delay(1000).fadeOut();
});
