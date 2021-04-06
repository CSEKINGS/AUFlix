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

function videocard() {
    var card = "";
    var config = {
        apiKey: "AIzaSyB2jAveBDZ6m8YBKEh1iCP2xJLLSeFoYyA",
        authDomain: "auflix-67633.firebaseapp.com",
        databaseURL: "https://auflix-67633-default-rtdb.firebaseio.com",
        projectId: "auflix-67633",
        storageBucket: "auflix-67633.appspot.com",
        messagingSenderId: "757795130164",
        appId: "1:757795130164:web:d2dd6d191911a0a7977361"
    };
    firebase.initializeApp(config);
    firebase.database().ref('test/').once('value', function (videos) {
        videos.forEach(function (data) {
            vid = data.val().id;
            card += "<div class='vcont' id='" + vid + "'><img src='https://img.icons8.com/metro/26/ffffff/close-window.png' class='close' onclick='yclose(\"" + vid + "\")' /><div class='tmpl' onclick='playvideo(\"" + vid + "\")'><img src='https://i.ytimg.com/vi/" + vid + "/maxresdefault.jpg'></div><img src='https://img.icons8.com/material-sharp/24/000000/dots-loading--v3.png' class='cont-opt'><div class='cont-panel' onclick='playvideo(\"" + vid + "\")'><h3>" + data.val().title + "</h3><h4>" + data.val().description + "</h4></div></div>";
        });
        document.getElementById("cardlist").innerHTML = card;
    });
}