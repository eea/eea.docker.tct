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

  self.open = function (target) {
    $(self).trigger({
      'type': 'modalopen',
      'target': target
    });
    self.activeModal = target;
    $(target).addClass('active');
    $('body').addClass('modal-open');
  };

  self.close = function () {
    target = self.activeModal;
    self.activeModal = null;
    $(target).removeClass('active');
    $('body').removeClass('modal-open');
  };

  // events - buttons
  $('[data-modal]').on('click', function (e) {
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
          beforeSend: function () {
            $(target).html('loading');
          }
        }).done(function (html) {
          $(target).html(html);
        });
      }
      self.open(target);
    }
  });
  // events - close
  $(self.activeModal).on('click', function (event) {
    event.stopPropagation();
  });
  $(self.container).on('click', function () {
    if (self.activeModal) {
      self.close();
    }
  });
  $(document).keyup(function (e) {
    if (e.keyCode == 27 && self.activeModal) {
      self.close();
    }
  });

  // TOC in goals was generating double ul - li markup

  // $('.toc ul').columnlist({
  //     size : 4,
  //     'class' : 'column-list',
  //     incrementClass : 'column-list-'
  // });
}

$(document).ready(function () {
  modal = new Modal($('.modal-container')[0]);
});

$(function () {
  $('.messages').delay(5000).fadeOut();
});

function showDescription(name, textSelector, url, type, code, value) {
  var selector = 'select[name=' + name + ']';
  $(selector).on('change', function () {
    var text = $(this).parents('.form-group').find(textSelector);
    text.html('');
    $("option:selected", this).each(function () {
      $.get(url.replace('1', this.value), function (data) {
        data = $.parseJSON(data)[0];
        if (code) {
          var title = '<h5>' + type + ' ' + data.code;
          if (data.title && data.value) {
            title += ': ' + data.title;
            title += '</h5>';
          }
          if (data.title && !data.value) {
            title += '</h5>';
            title += '<p>' + data.title + '</p>';
          }
          text.append(title);
        }
        if (data.value) {
          text.append('<p>' + data.value + '</p>');
        }
      });
    });
  }).change();
}

function showTargetValue(name, textSelector, url) {
  showDescription(name, textSelector, url, 'Target', false, true);
}

function showTargetCodeValue(name, textSelector, url) {
  showDescription(name, textSelector, url, 'Target', true, true);
}

function showIndicatorCodeValue(name, textSelector, url) {
  showDescription(name, textSelector, url, 'EU Indicator', true, true);
}

function showObjectiveCodeValue(name, textSelector, url) {
  showDescription(name, textSelector, url, 'Objective', true, true);
}

function showActionCodeValue(name, textSelector, url) {
  showDescription(name, textSelector, url, 'Action', true, true);
}

function forbidChoicesIntersection(selector1, selector2) {
  $(selector1).on('change', function () {
    $("option", this).each(function () {
      var option2 = $(selector2).find('option[value=' + this.value + ']');
      if (this.selected) {
        option2.hide();
      }
      else {
        option2.show();
      }
    });
    $(selector2).trigger('chosen:updated');
  }).change();
}

function forbidCrossChoicesIntersection(name, nameOther) {
  var selectorTargets = 'select[name=' + name + ']';
  var selectorOtherTargets = 'select[name=' + nameOther + ']';

  forbidChoicesIntersection(selectorTargets, selectorOtherTargets);
  forbidChoicesIntersection(selectorOtherTargets, selectorTargets);
}




