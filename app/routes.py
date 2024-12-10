import os
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from webcolors import hex_to_rgb

from app import app
from app.forms import UploadForm
from app.utils.kmeans import Kmeans
from app.utils.knn import Knn

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    form = UploadForm()
    return render_template("index.html", form=form)


@app.route("/get_palette", methods=["POST"])
def palette():
    if "clusters" not in request.form:
        return jsonify({"message": "No number of clusters specified"}), 400
    if "image" not in request.files or request.files["image"].filename == "":
        return jsonify({"message": "No file selected for uploading"}), 400

    file = request.files["image"]

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOADS_DEFAULT_DEST"], filename)
        file.save(filepath)

        try:
            cluster_n = int(request.form.get("clusters"))
        except ValueError:
            os.remove(filepath)
            return jsonify({"message": "Invalid number of clusters"}), 400

        kmeans = Kmeans(filepath, cluster_n)
        color_hex = kmeans.get_tints()

        color_names = []
        knn = Knn()
        for color in color_hex:
            r, g, b = hex_to_rgb(color)
            name = knn.get_color_name(r, g, b)
            color_names.append(name)

        os.remove(filepath)

        return (
            jsonify(
                {
                    "message": "File successfully uploaded",
                    "colors": color_hex,
                    "names": color_names,
                }
            ),
            201,
        )
    else:
        return jsonify({"message": "Allowed file types are png, jpg, jpeg"}), 400
