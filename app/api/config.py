import os
current_dir = os.path.dirname(__file__)
basedir = os.path.abspath(os.path.join(current_dir, os.pardir))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'db', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
