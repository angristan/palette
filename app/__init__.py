from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from app import routes
