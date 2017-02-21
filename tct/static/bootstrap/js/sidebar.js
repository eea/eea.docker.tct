$(document).ready(function() {

    $navtrigger = $(".nav-trigger button");
    $navcontainer = $(".nav-container");
    $closetrigger = $(".close-trigger");
    $sidebartrigger = $('.sidebar-trigger button');
    $sidebarright = $('.sidebar-right');
    $accountheader = $('.account-menu-header');
    $accountmenu = $('.account-menu');
    $backdrop = $('#backdrop');
    $sidebar = $('.sidebar');
    $langheader = $('.lang-menu-header');
    $langmenu = $('.lang-menu');
    var toggle_user = 0;
    var toggle_lang = 0;


    $('.nav-trigger button, .close-trigger').click(function() {
        $backdrop.animate({
            height: 'toggle'
        }, 1);
        $('body').toggleClass('sidebaropen');
        $navcontainer.animate({
            width: 'toggle'
        }, 120);
    });


    $('.sidebar-trigger button').click(function() {
        $backdrop.animate({
            height: 'toggle'
        }, 1);
        $('body').toggleClass('sidebaropen');
        $sidebarright.animate({
            width: 'toggle'
        }, 120);
        $sidebar.animate({
            width: 'toggle'
        }, 120);
    });


    $backdrop.click(function() {
        $backdrop.toggle();
        $sidebarright.animate({
            width: 'hide'
        }, 120);
        $navcontainer.animate({
            width: 'hide'
        }, 120);
        $accountmenu.animate({
            height: 'hide'
        }, 120);
        $sidebar.animate({
            width: 'hide'
        }, 120);
        $('body').removeClass('sidebaropen');
    });


    $('body').click(function(e) {

        if ($(e.target).hasClass('lang-menu-trigger')) {
            $('.lang-menu').animate({
                height: 'toggle'
            }, 120);
            $('.lang-menu-header').toggleClass('clicked');
        } else {
            $('.lang-menu').animate({
                height: 'hide'
            }, 120);
            $('.lang-menu-header').removeClass('clicked');
        }

        if ($(e.target).parent().hasClass('goals-menu-header')) {
            $('.goals-menu').animate({
                height: 'toggle'
            }, 120);
            // $('.goals-menu-header a').toggleClass('clicked');
        } else {
            $('.goals-menu').animate({
                height: 'hide'
            }, 120);
            // $('.goals-menu-header a').removeClass('clicked');
        }

    });




    $('body').click(function(e) {
        if ($(e.target).hasClass('account-menu-trigger')) {
            $('.account-menu').animate({
                height: 'toggle'
            }, 120);
            $('.account-menu-header').toggleClass('clicked');
        } else {
            $('.account-menu').animate({
                height: 'hide'
            }, 120);
            $('.account-menu-header').removeClass('clicked');
        }

    });


    var numberofsidebars = $('.sidebar-right').length + $('.sidebar').length;
    if (numberofsidebars == 1) {
        $('.main').addClass('one-sidebar');
    } else if (numberofsidebars == 0) {
        $('.main').addClass('no-sidebar');
    }
    if ($('.main').hasClass('no-sidebar')) {

        $(".sidebar-trigger").remove();
    }


    $sidebargoal = $(".sidebar-menu #list-item > a");
    $sidebargoalmenu = $(".sidebar-menu > li ");
    $sidebargoal.click(function(e) {
        var $trigger_sidemenu = $(this);
        $testes = $(this).parent().find('.sidebar-submenu').first();
        $testes.animate({
            height: 'toggle'
        }, 320);
    });


    var adjustAnchor = function() {
        var $anchor = $(':target'),
            navbarheight = 120;
        if ($anchor.length > 0) {
            $('html, body')
                .stop()
                .animate({
                    scrollTop: $anchor.offset().top - navbarheight
                }, 250);
        }
    };


    $(window).on('hashchange', function() {
        adjustAnchor();
    });


    $('.sidebar-submenu a').click(function() {
        adjustAnchor();
    });


    setTimeout(function() {
        if (document.location.hash || window.hashchange) {
            adjustAnchor();
        }
    }, 300);


    $('.search').on('focus', function() {
        $('.sidebar-submenu').addClass('visible');
    });

    $(document).click(function(e) {
        if (!($(e.target).hasClass('search') || $(e.target).hasClass('nat-objective'))) {
            $('.sidebar-submenu').removeClass('visible');
        }
    });

});
