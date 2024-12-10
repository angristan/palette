import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_uploads import IMAGES, UploadSet, configure_uploads

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

if app.config["LOG_TO_STDOUT"]:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/api.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

bootstrap = Bootstrap4(app)

images = UploadSet("images", IMAGES)
configure_uploads(app, images)

from app import routes
