import os

from flask import render_template, request
from flask.helpers import url_for
from werkzeug import redirect, secure_filename

from app import app, images
from app.forms import UploadForm
from app.utils.kmeans import get_tints


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

        print(get_tints(filepath))

        print("good")
        return redirect(url_for('index'))

    return redirect(url_for('index'))
