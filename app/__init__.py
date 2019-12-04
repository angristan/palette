from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from app import routes
