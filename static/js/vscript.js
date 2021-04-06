function yclose(id) {
    val = document.getElementById(id);
    val.className = "vcont";
    val.getElementsByClassName("tmpl")[0].innerHTML = "<img src='https://i.ytimg.com/vi/" + id + "/maxresdefault.jpg'>";
    val.getElementsByClassName("close")[0].style.display = "none";
}

function playvideo(id) {
    val = document.getElementById(id);
    val.className = "fulscrn";
    val.getElementsByClassName("tmpl")[0].innerHTML = "<iframe src='https://www.youtube.com/embed/" + id + "'></iframe>";
    val.getElementsByClassName("close")[0].style.display = "block";
}

function ghover(id) {
    var val = document.getElementById(id).src;
    document.getElementById(id).src = val.replace(".png", ".gif")
}

function gout(id) {
    var val = document.getElementById(id).src;
    document.getElementById(id).src = val.replace(".gif", ".png")
}
