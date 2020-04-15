import sqlite3
from flask import Flask
from config import Config


app = Flask(__name__)
con = sqlite3.connect('../db/app_sql.db', isolation_level=None)
con.row_factory = sqlite3.Row  # supports mapping access by column name and index, iteration, etc


@app.shell_context_processor
def make_shell_context():
    return {'con': db}


# keep this at the bottom to avoid circular dependencies
import routes, models
