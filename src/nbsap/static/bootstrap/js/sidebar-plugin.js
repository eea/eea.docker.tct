function sidebarplugin($trigger, $sidebar, $closetrigger) {

    console.log('plugin works');
    $body = $("body");
    $backdrop = $('#backdrop');
    $trigger.click(function() {
        // console.log($sidebar);
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

