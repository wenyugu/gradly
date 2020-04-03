import time
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)  # all config options are specified in an external file
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

# keep this at the bottom to avoid circular dependencies
import routes, models
