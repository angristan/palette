const form = document.getElementById('file-form');
const fileSelect = document.getElementById('upload');
const uploadButton = document.getElementById('submit');
const progressbar = document.getElementById('progress-bar');
const progressdiv = document.getElementById('progress-div');
const tintslisttable = document.getElementById('tints');
const tintslistdiv = document.getElementById('tints-list');

form.onsubmit = function (event) {
  event.preventDefault();
  progressdiv.style.display = "block";
  uploadButton.innerHTML = 'Uploading...';

  const files = fileSelect.files;
  const formData = new FormData();
  const file = files[0];
  formData.append('image', file, file.name);
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'get_palette', true);
  xhr.upload.onprogress = function (e) {
    update_progress(e);
  }
  xhr.onload = function (e) {
    if (xhr.status === 201) {
      uploadButton.innerHTML = 'Upload';

      const response = JSON.parse(xhr.response);
      console.log(response.colors)

      tintslistdiv.style.display = 'block';

      for (color = 0; color < response.colors.length; color++) {
        const tr = document.createElement("tr");
        const th = document.createElement("th");
        const tdColorValue = document.createElement("td");
        const tdColorName = document.createElement("td");

        th.scope = "row";
        th.innerText = color;
        tdColorValue.innerText = response.colors[color];
        tdColorName.innerText = response.names[color];

        tr.appendChild(th);
        tr.appendChild(tdColorValue);
        tr.appendChild(tdColorName);
        tr.style.color = response.colors[color];

        tintslisttable.appendChild(tr);
      }
    } else {
      alert('An error occurred!');
    }
  };
  xhr.send(formData);
}
function update_progress(e) {
  if (e.lengthComputable) {
    const percentage = Math.round((e.loaded / e.total) * 100);

    progressbar.style.width = percentage + '%';

    uploadButton.innerHTML = 'Upload ' + percentage + '%';
    console.log("percent " + percentage + '%');
  }
  else {
    console.log("Unable to compute progress information since the total size is unknown");
  }
}





