import os
import numbers

from flask import render_template, request, abort
from flask.helpers import url_for
from werkzeug import redirect, secure_filename

from app import app
from app import images
from app.forms import UploadForm
from app.utils.kmeans import get_tints
from app.utils.knn import Knn
from webcolors import hex_to_rgb
from flask.json import jsonify

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/get_palette', methods=['POST'])
def palette():
    print(type(request.form.get('clusters')))
    if 'clusters' not in request.form:
        resp = jsonify({'message' : 'No number of clusters specified'})
        resp.status_code = 400
        return resp
    if 'image' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['image']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
        file.save(filepath)
        cluster_n = int(request.form.get('clusters'))
        color_hex = get_tints(filepath, cluster_n)
        print(color_hex)
        color_names = [];

        for color in color_hex:
            r,g,b = hex_to_rgb(color)
            name = Knn().get_color_name(r,g,b)
            color_names.append(name)

        print(color_names)


        resp = jsonify({'message' : 'File successfully uploaded', 'colors' : color_hex, 'names': color_names})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 400
        return resp
