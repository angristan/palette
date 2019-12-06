from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.simple import SubmitField

from app import images
from app import app


class UploadForm(FlaskForm):
    upload = FileField('Choose an image...', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])
    submit = SubmitField('Analyse image')
