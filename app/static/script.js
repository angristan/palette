var form = document.getElementById('file-form');
var fileSelect = document.getElementById('upload');
var uploadButton = document.getElementById('submit');

form.onsubmit = function(event) {
  event.preventDefault();
  var progress = document.getElementById('progress');
  var progressdiv = document.getElementById('progressdiv');
  progress.style.display = "block";
  uploadButton.innerHTML = 'Uploading...';
  var files = fileSelect.files;
  var formData = new FormData();
  var file = files[0];
  formData.append('image', file, file.name);
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'get_palette', true);
  xhr.upload.onprogress = function (e) {
    update_progress(e);
  }
  xhr.onload = function (e) {
    if (xhr.status === 201) {
      uploadButton.innerHTML = 'Upload';
      progressdiv.innerHTML = "<h3>Sucess</h3>";

      const response = JSON.parse(xhr.response);
      console.log(response.colors)

      const tints_list = document.getElementById('tints');

      for(color = 0; color < response.colors.length; color++) {
          const node = document.createElement("li");
          const textnode = document.createTextNode(response.colors[color]);
          node.appendChild(textnode);
          node.style.color = response.colors[color];
          tints_list.appendChild(node);
      }
    } else {
      alert('An error occurred!');
    }
  };
  xhr.send(formData);
}
function update_progress(e){
    if (e.lengthComputable){
        var percentage = Math.round((e.loaded/e.total)*100);
        progress.value = percentage;
        uploadButton.innerHTML = 'Upload '+percentage+'%';
        console.log("percent " + percentage + '%' );
    }
    else{
      console.log("Unable to compute progress information since the total size is unknown");
    }
}





