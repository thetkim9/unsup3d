function check_progress(task_id, progress_bar) {
  $("#progress_bar").hide();
      $.get('progress/' + task_id, function(data) {
          document.body.innerHTML += data;
          if (progress < 100) {
              document.body.innerHTML += progress;
              progress_bar.set_progress(progress);
              setInterval(check_progress, 1000);
          }
      })
}
document.getElementById("submit").onclick = () => {
    var formData = new FormData();
    var source = document.getElementById('source').files[0];
    //const { v4: uuidv4 } = require('uuid');
    //var user_id = uuidv4();
    var user_id = Math.floor(Math.random()*1000000000);
    document.body.innerHTML += user_id;
    var progress_bar = document.getElementById('progress_bar');
    formData.append('person_image', source);
    formData.append('user_id', user_id);
    check_progress(user_id, progress_bar);
    fetch(
        '/render3D',
        {
            method: 'POST',
            body: formData,
        }
    )
    .then(response => {
        if ( response.status == 200){
            return response
        }
        else{
            document.body.innerHTML += response.status
            throw Error("rendering error")

        }
    })
    .then(response => response.blob())
    .then(blob => URL.createObjectURL(blob))
    .then(imageURL => {
        document.getElementById("result").src = imageURL;
        document.getElementById("errorbox").innerHTML = "";
    })
    .catch(e =>{
        document.getElementById("errorbox").innerHTML = e;
    })
}
