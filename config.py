import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOADS_DEFAULT_DEST') or '/tmp'
