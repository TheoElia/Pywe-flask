var myIndex = 0;

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    var c = document.getElementsByClassName("caption");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";
    }
    for (i = 0; i < c.length; i++){
     c[i].style.display = "none";
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}
    x[myIndex-1].style.display = "block";
    c[myIndex-1].style.display = "block";
    setTimeout(carousel, 5000); // Change image every 5 seconds
}