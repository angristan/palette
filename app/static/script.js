const form = document.getElementById("file-form");
const fileSelect = document.getElementById("upload");
const progressbar = document.getElementById("progress-bar");
const progressdiv = document.getElementById("progress-line");
const tintslisttable = document.getElementById("tints");
const tintslistdiv = document.getElementById("tints-list");
const statusBadge = document.getElementById("badge-status");

form.onsubmit = function (event) {
  event.preventDefault();

  // If no file has been selected, don't do anything
  if (fileSelect.files.length === 0) {
    return;
  }

  // Hide and clear result table forsubsequent uploads
  // This will not change anything for the first upload when the page is clean
  tintslistdiv.style.display = "none";
  tintslisttable.innerHTML = "";
  statusBadge.innerText = "Uploading...";
  statusBadge.className = "badge badge-primary col-sm-2";

  // Show progress bar for the first upload
  progressdiv.style.display = "flex";

  const clusters = document.getElementById("clusters");
  const files = fileSelect.files;
  const formData = new FormData();
  const file = files[0];
  formData.append("image", file, file.name);
  formData.append("clusters", clusters.value);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "get_palette", true);
  xhr.upload.onprogress = function (e) {
    update_progress(e);
  };
  xhr.onload = function (e) {
    if (xhr.status === 201) {
      const response = JSON.parse(xhr.response);
      console.log(response.colors);

      tintslistdiv.style.display = "block";

      for (color = 0; color < response.colors.length; color++) {
        const tr = document.createElement("tr");
        const th = document.createElement("th");
        const tdColorValue = document.createElement("td");
        const tdColorName = document.createElement("td");

        th.scope = "row";
        th.innerText = color + 1;
        tdColorValue.innerText = response.colors[color];
        tdColorName.innerText = response.names[color];

        tr.appendChild(th);
        tr.appendChild(tdColorValue);
        tr.appendChild(tdColorName);
        tr.style.color = response.colors[color];

        tintslisttable.appendChild(tr);
      }

      statusBadge.innerText = "Done.";
      statusBadge.className = "badge badge-success col-sm-2";
    } else {
      statusBadge.innerText = "Error.";
      statusBadge.className = "badge badge-danger col-sm-2";
    }
  };
  xhr.send(formData);
};
function update_progress(e) {
  if (e.lengthComputable) {
    const percentage = Math.round((e.loaded / e.total) * 100);

    progressbar.style.width = percentage + "%";

    if (percentage == 100) {
      // When upload is done, the backend is working...
      statusBadge.innerText = "Processing...";
      statusBadge.className = "badge badge-warning col-sm-2";
    }
  } else {
    console.log("Unable to compute progress information since the total size is unknown");
  }
}
