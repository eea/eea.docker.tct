$(document).ready(function() {

    setTimeout(function() {
        $('.homepage-info').fadeTo("fast", 1);
    setTimeout(function() {
        $('.homepage-info').removeClass('info-translated')
        setTimeout(function() {
            $('#trigger-overlay').fadeTo("fast", 1);
        }, 1500);
    }, 500);
  }, 500);


    $(".overlay").prependTo("body");
    $trigger = $('#trigger-overlay');
    $overlay = $('.overlay');
    $close = $('.overlay-close');
    $container = $('.container');

    $trigger.on('click', function() {
        $overlay.addClass('display').delay(1).queue(function() {
            $overlay.addClass('open');
            $container.addClass('overlay-open');
            $overlay.dequeue();
            $container.dequeue();
        });
    })

    $close.on('click', function() {
        $overlay.removeClass('open').delay(500).queue(function() {
            $overlay.removeClass('display');
            $overlay.dequeue();

        });
        $container.removeClass('overlay-open');
    })

});
