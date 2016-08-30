$(document).ready(function() {

    $navtrigger = $(".nav-trigger button");
    $navcontainer = $(".nav-container");
    $closetrigger = $(".close-trigger");
    $sidebartrigger = $('.sidebar-trigger button');
    $sidebarright = $('.sidebar-right')
    $accountheader = $('.account-menu-header');
    $accountmenu = $('.account-menu');
    $backdrop = $('#backdrop');
    var toggle = 0;
    // sidebarplugin($navtrigger, $navcontainer, $closetrigger)

    // sidebarplugin($sidebartrigger, $sidebarright, $closetrigger)

    $accountheader.click(function() {

    	$accountheader.toggleClass('clicked');


        $accountmenu.animate({
            height: 'toggle'
        },120);

        toggle++;

        if (toggle == 1) {
        $('#user-close').animate({ borderSpacing: 90 }, {
            step: function(now, fx) {
                $(this).css('-webkit-transform', 'rotate(' + now + 'deg)');
                $(this).css('-moz-transform', 'rotate(' + now + 'deg)');
                $(this).css('transform', 'rotate(' + now + 'deg)');
            }
        });
    }

        if (toggle != 1) {
            $('#user-close').animate({ borderSpacing: 0 }, {
                step: function(now, fx) {
                    $(this).css('-webkit-transform', 'rotate(' + now + 'deg)');
                    $(this).css('-moz-transform', 'rotate(' + now + 'deg)');
                    $(this).css('transform', 'rotate(' + now + 'deg)');
                    toggle = 0;
                }
            });
        }

    });


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
        },120);
    });


    $backdrop.click(function() {

        $backdrop.toggle();
        $sidebarright.animate({
            width: 'hide'
        },120);
        $navcontainer.animate({
            width: 'hide'
        },120);

         $accountmenu.animate({
            height: 'hide'
        },120);

        $('body').removeClass('sidebaropen');

    });



    $targetlistorder=$('.target-list li .target-code');
    $targetlistorder.each(function(){

if ($(this).text().match(/[a-z]/i)) {
    $(this).parent().css("padding-left","25px");
}

        });

    var numberofsidebars= $('.sidebar-right').length + $('.sidebar').length;
 if (numberofsidebars == 1) {
    $('.main').addClass('one-sidebar');
    }
    else if (numberofsidebars == 0){
         $('.main').addClass('no-sidebar');
    }

});
