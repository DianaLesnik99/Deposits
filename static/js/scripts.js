/*Down and Up Buttons*/
jQuery(function () {
    $(".GoTop").hide();
    if ($(window).scrollTop() >= 250) $(".GoTop").fadeIn("slow")
    $(window).scroll(function () {
        if ($(window).scrollTop() <= 550) $(".GoTop").fadeOut("slow")
        else $(".GoTop").fadeIn("slow")
    });

    $(".GoBottom").hide();
    if ($(window).scrollTop() <= $(document).height() - "999") $(".GoBottom").fadeIn("slow")
    $(window).scroll(function () {
        if ($(window).scrollTop() >= $(document).height() - "999") $(".GoBottom").fadeOut("slow")
        else $(".GoBottom").fadeIn("slow")
    });

    $(".GoTop").click(function () {
        $("html, body").animate({scrollTop: 0}, "slow")
    })

    $(".GoBottom").click(function () {
        $("html, body").animate({scrollTop: $(document).height()}, "slow")
    })
});
/*Down and Up Buttons*/

/*Print document*/
const button = document.querySelector('.print')
function handleClick() {
  window.print();
}
button.addEventListener('click', handleClick)
/*Print document*/
