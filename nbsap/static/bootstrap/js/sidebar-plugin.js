function sidebarplugin($trigger, $sidebar, $closetrigger) {


    $body = $("body");
    $backdrop = $('#backdrop');
    $trigger.click(function() {
        $sidebar.addClass('nav-open')
        $body.addClass('sidebaropen');
        $backdrop.addClass('open');
    });

    $backdrop.click(function() {
        $sidebar.removeClass('nav-open')
        $body.removeClass('sidebaropen');
        $backdrop.removeClass('open');
    });

    $closetrigger.click(function() {
        $sidebar.removeClass('nav-open')
        $body.removeClass('sidebaropen');
        $backdrop.removeClass('open');
    });
}

