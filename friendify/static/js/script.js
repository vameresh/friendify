
function slideCompare(user, duration){
    info = $(document.getElementById(user + "-info")); 
    arrow = $(document.getElementById(user + "-arrow")); 
    arrow.toggleClass("rotate")
    info.slideToggle( duration, function() {
        // Animation complete.
      });
}

$(document).ready(function (){
    $('.follow').each(function () {
        slideCompare(this.id, 1);
    });
});