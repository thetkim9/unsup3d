const controller;
document.body.onload = function() {
    document.getElementById("load").style.visibility = "hidden";
    if (timer!=null)
        clearInterval(timer);
    if (controller!=null)
        controller.abort();
    //$.get('stopsubp/' + user_id);
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
    formData.append('user_id', user_id);
    $.get('setup/' + user_id);
    check_progress(user_id, progress_bar);
    controller = new AbortController()
    const { abort } = controller;
    fetch(
        '/render3D',
        {
            method: 'POST',
            body: formData,
            signal: abort
        }
    )
    .then(response => {
        if ( response.status == 200){
            return response
        }
        else{
            document.body.innerHTML += response.status
            throw Error("rendering error:")
        }
    })
    .then(response => response.blob())
    .then(blob => URL.createObjectURL(blob))
    .then(imageURL => {
        document.getElementById("result").src = imageURL;
        document.getElementById("errorbox").innerHTML = "";
        $.get('remove/' + user_id);
        submit.style.visibility = "visible";
    })
    .catch(e =>{
        document.getElementById("errorbox").innerHTML = e;
    })
}
