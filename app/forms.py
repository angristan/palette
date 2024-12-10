from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField
from wtforms.fields.simple import SubmitField

from app import images


class UploadForm(FlaskForm):
    upload = FileField(
        "Choose an image...",
        validators=[FileRequired(), FileAllowed(images, "Images only!")],
    )
    clusters = IntegerField(
        "clusters",
    )
    submit = SubmitField("Analyse image")
