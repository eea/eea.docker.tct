



$(document).ready(function() {

$navtrigger=$(".nav-trigger button");
$navcontainer= $(".nav-container");
$closetrigger= $(".close-trigger");
$sidebartrigger= $('.sidebar-trigger button');
$sidebarright=$('.sidebar-right')

sidebarplugin($navtrigger, $navcontainer, $closetrigger)

sidebarplugin($sidebartrigger, $sidebarright, $closetrigger)
});