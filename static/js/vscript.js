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

function searchBox(id){
    sc=document.getElementById("searchbox");
    if(sc.className == "searchbox"){
        sc.className="hide"
    }else{
        sc.className="searchbox";
    }
}

function searchKey() {
    showlist = []
    outlist = document.getElementsByClassName('outer-list');
    key = document.getElementById("searchkey").value.split(" ")
    for (var j = 0; j < outlist.length; j++) {
        vcont = outlist[j].getElementsByClassName('vcont');
        lkey=document.getElementsByClassName('tags');
        for (var k = 0; k < key.length; k++) {
            outlist[j].style.display = "none";
            lkey[j].style.display="none";
            for (var i = 0; i < vcont.length; i++) {
                if (vcont[i].getElementsByTagName('key')[0].innerText.indexOf(key[k]) > -1) {
                    vcont[i].style.display = "";
                    outlist[j].style.display = "";
                    lkey[j].style.display="";
                }
            }
        }
    }
}