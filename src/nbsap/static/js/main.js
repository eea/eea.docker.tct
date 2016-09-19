$(function() {
    $('.change-lang').on('click', function() {
        $(this).parent().find('form').submit();
    });

    var indicator_modal = $('#indicator_modal');
    indicator_modal.on('hidden', function() {
        indicator_modal.data('modal', false);
        indicator_modal.html('');
    });

});


function toggleClassMenu() {
    $('.modal-container .container').addClass('menu--animatable');
    var layout = $(".modal-window");
    if (!layout.hasClass("trans-open")) {
        layout.addClass("trans-open");
    } else {
        layout.removeClass("trans-open");
    }
};

function OnTransitionEnd() {
    $('.modal-container .container').removeClass("menu--animatable");
}



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
        $('.modal-container').show(function() {
            toggleClassMenu();
        });

    };

    self.close = function() {
        target = self.activeModal;
        self.activeModal = null;
        $('.modal-container .container').on("transitionend", OnTransitionEnd);
        $(target).on("click", toggleClassMenu());
        $('.modal-container').hide(600);
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

    $(document).ready(function() {
        $('.modal-container').on('click', ".modal-bot", function() {
            self.close();
        });

    });

    $(document).keyup(function(e) {
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


$(document).ready(function() {
    modal = new Modal($('.modal-container')[0]);
});

$(function() {
    // $('.messages').delay(5000).fadeOut();

    $('.messages').delay(4000).animate({
        width: 'hide'
    }, 200);




});

function showDescription(name, textSelector, url, type, code, value) {
    var selector = 'select[name=' + name + ']';
    $(selector).on('change', function() {
        var text = $(textSelector);
        text.html('');
        $("option:selected", this).each(function() {
            $.get(url.replace('1', this.value), function(data) {
                data = $.parseJSON(data)[0];
                if (code) {
                    var title = '<li><i class="fa"></i><div class="timeline-item"><h3 class="timeline-header">' + type + ' ' + data.code + '</h3>';
                    if (data.title && data.value) {
                        title += ': ' + data.title;
                        title += '</div>';
                    }
                    if (data.title && !data.value) {
                        title += '</h3>';
                        title += '<div class="timeline-body">' + data.title + '</div></div></li>';
                    }
                }
                if (data.value) {
                    title += '<div class="timeline-body">' + data.value + '</div></div></li>';
                }
                text.append(title);
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

function showEuTargetCodeValue(name, textSelector, url) {
    showDescription(name, textSelector, url, 'EU Target', true, true);
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
    $(selector1).on('change', function() {
        if (this.value) {
            $("option", this).each(function() {
                var option2 = $(selector2).find('option[value=' + this.value + ']');
                if (this.selected) {
                    option2.hide();
                } else {
                    option2.show();
                }
            });
            $(selector2).trigger('chosen:updated');
        }
    }).change();
}

function forbidCrossChoicesIntersection(name, nameOther) {
    var selectorTargets = 'select[name=' + name + ']';
    var selectorOtherTargets = 'select[name=' + nameOther + ']';

    forbidChoicesIntersection(selectorTargets, selectorOtherTargets);
    forbidChoicesIntersection(selectorOtherTargets, selectorTargets);
}
