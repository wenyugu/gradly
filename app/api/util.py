from api import app, con


def log_error(e: Exception):
    app.logger.error('{}: {}'.format(type(e).__name__, e))


# Explicit transaction management
def tx_begin():
    con.execute('BEGIN')


def tx_commit():
    con.commit()


def tx_rollback():
    con.rollback()
