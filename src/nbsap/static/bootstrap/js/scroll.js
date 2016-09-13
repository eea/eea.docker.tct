//capture scroll any percentage

$(document).ready(function () {
$(window).scroll(function(){

    var wintop = $(window).scrollTop(), docheight = $(document).height(), winheight = $(window).height();
    var  scrolltrigger = 0.95;
    var scrolled = +(wintop/(docheight-winheight))*100;
    // console.log('wintop='+wintop);
    // console.log('docheight='+docheight);
    // console.log('winheight='+winheight);
    // console.log(wintop+'=='+(docheight-winheight));
    // console.log(wintop==(docheight-winheight));
    // console.log('%scrolled='+(wintop/(docheight-winheight))*100);
    // console.log(scrolled);
    // if  ((wintop/(docheight-winheight)) > scrolltrigger) {
    //    console.log('scroll bottom');
    // }
if (scrolled >= 80) {
	$('.pages-navigation').animate({
      height: 'show'
    }, 200);
}
else {

$('.pages-navigation').animate({
      height: 'hide'
    }, 200);

}
// if (scrolled == NaN) {
// 		$('.pages-navigation').animate({
//       height: 'show'
//     }, 200);
// }

});

 if ($("body").height() < $(window).height()) {
        $('.pages-navigation').animate({
      height: 'show'
    }, 200);
    }



});