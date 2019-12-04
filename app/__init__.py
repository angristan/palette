import logging
import os
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)

if app.config['LOG_TO_STDOUT']:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/api.log',
                                        maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

bootstrap = Bootstrap(app)

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

from app import routes
