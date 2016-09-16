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



    // $targetlistorder = $('.target-list li .target-code');
    // $targetlistorder.each(function () {

    //   if ($(this).text().match(/[a-z]/i)) {
    //     $(this).parent().css("padding-left", "25px");
    //   }

    // });

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
        console.log($(e.target));


        $testes.animate({
            height: 'toggle'
        }, 320);
    });


    // $('.sidebar-trigger').click(function(){
    //   console.log('trololo');
    //   $sidebartrigger.removeClass('no-events');
    //   $(this).addClass('sidebar-trigger-triggered ');
    // })

    // $(window).resize(function() {
    //     // run test on initial page load
    //     checkSize();

    //     // run test on resize of the window
    //     $(window).resize(checkSize);
    // });

    // //Function to the css rule
    // function checkSize(){
    //     if ($(".nav-trigger button").css("display") == "block" ){

    //     $('.sidebar').addClass('sidebar-right');
    //     $('.sidebar-right').removeClass('sidebar');

    //     }
    // }

    // (function() {
    //  $(window).on("load", function() {


    //     if (document.location.hash || window.hashchange) {
    //       console.log('are');
    //         setTimeout(function() {
    //             window.scrollTo(window.scrollX, window.scrollY - 130);
    //         }, 10);
    //     }

    //     $('.sidebar-menu a').click(function(){
    //        if (document.location.hash) {
    //         setTimeout(function() {
    //             window.scrollTo(window.scrollX, window.scrollY - 130);
    //         }, 10);
    //     }
    //     })
    //   })

    // })();

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

    $('body').click(function(e) {
        if (!($(e.target).hasClass('search') || $(e.target).hasClass('nat-objective'))) {
            $('.sidebar-submenu').removeClass('visible');
        }
    });


});
