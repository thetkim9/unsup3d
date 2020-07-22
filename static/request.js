var controller;
document.body.onload = function() {
    document.getElementById("load").style.visibility = "hidden";
}
window.onbeforeunload = function() {
    if (timer!=null) {
        clearInterval(timer);
    }
    if (controller!=null) {
        //alert("abort");
        controller.abort();
    }
    $.get('remove/' + user_id);
    return "Do you really want to leave this page?";
}
var timer;
function check_progress(task_id, progress_bar) {
    document.getElementById("load").style.visibility = "visible";
    var progress_bar = document.getElementById("progress_bar");
    var dots = document.getElementById("dots");
    var time_spent = document.getElementById("time");
    var temp = [".", "..", "..."];
    var time = 0;
    function worker() {
      $.get('progress/' + task_id, function(progress) {
          progress_bar.value = Math.min(parseInt(progress), 100).toString();
          time += 1;
          time_spent.innerHTML = time;
          dots.innerHTML = temp[time%3];
          if (parseInt(progress)>=100) {
            dots.innerHTML = " complete";
            clearInterval(timer);
            alert(progress_bar.value);
          }
      })
    }
    timer = setInterval(worker, 1000);
}

document.getElementById("submit").onclick = () => {
    document.getElementById("result").src = "";
    var formData = new FormData();
    var source = document.getElementById('source').files[0];
    var submit = document.getElementById('submit');
    submit.style.visibility = "hidden";
    //const { v4: uuidv4 } = require('uuid');
    //var user_id = uuidv4();
    var user_id = Math.floor(Math.random()*1000000000);
    var progress_bar = document.getElementById('progress_bar');
    formData.append('person_image', source);
    //formData.append('user_id', user_id);
    $.get('setup/' + user_id);
    check_progress(user_id, progress_bar);
    controller = new AbortController();
    var abort = controller.signal;
    fetch(
        '/render3D/'+user_id,
        {
            method: 'POST',
            body: formData,
            signal: abort
        }
    )
    .then(response => {
        if ( response.status == 200){
            return response;
        }
        else{
            throw Error("rendering error:");
        }
    })
    .then(response => {
        if (parseInt(response.headers['user_id']) == user_id) {
            alert(response.headers['user_id']);
            return response.blob();
        }
        else
            throw Error("response to different user");
    })
    .then(blob => URL.createObjectURL(blob))
    .then(imageURL => {
        document.getElementById("result").src = imageURL;
        //document.body.innerHTML += imageURL;
        document.getElementById("errorbox").innerHTML = "";
        $.get('remove/' + user_id);
        submit.style.visibility = "visible";
    })
    .catch(e =>{
        if (e!="response to different user")
            document.getElementById("errorbox").innerHTML = e;
    })
}
