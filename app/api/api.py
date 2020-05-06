import sqlite3
from flask import Flask


app = Flask(__name__)
con = sqlite3.connect('../db/app.db')
# Default to autocommit mode.
# Manage explicit transactions using 'BEGIN', 'COMMIT', and 'ROLLBACK'
con.isolation_level = None
# supports mapping access by column name and index, iteration, etc
con.row_factory = sqlite3.Row
con.execute("PRAGMA foreign_keys = ON")


@app.shell_context_processor
def make_shell_context():
    return {'con': con}


# keep this at the bottom to avoid circular dependencies
import routes
