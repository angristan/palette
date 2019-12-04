import os

from flask import render_template, request, abort
from flask.helpers import url_for
from werkzeug import redirect, secure_filename

from app import app
from app import images
from app.forms import UploadForm
from app.utils.kmeans_scratch import get_colors
from flask.json import jsonify

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    form = UploadForm()
    return render_template('index.html', form=form)


@app.route('/upload', methods=['POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.upload.data
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOADS_DEFAULT_DEST'], filename)
        f.save(filepath)

        # Compute the 5 major tints
        tints = get_colors(filepath, 5)

        form = UploadForm()
        return render_template('index.html', form=form, tints=tints)

    return redirect(url_for('index'))

@app.route('/get_palette', methods=['POST'])
def palette():
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
        tints = get_colors(filepath, 5)
        resp = jsonify({'message' : 'File successfully uploaded', 'colors' : tints})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 400
        return resp
