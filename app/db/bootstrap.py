import os
import sqlite3

BASEDIR = os.path.dirname(__file__)

if os.path.isfile(os.path.join(BASEDIR, 'app.db')):
    print("Database 'app.db' already exits. Would you like to overwrite it?")
    resp = input('[y/N] ')

    if resp == 'y' or resp == 'Y':
        print('Removing old database')
        os.remove(os.path.join(BASEDIR, 'app.db'))
    else:
        print('Database exists, exiting')
        exit(0)

print("Creating database at 'app.db'")
con = sqlite3.connect(os.path.join(BASEDIR, 'app.db'))

with open(os.path.join(BASEDIR, 'schema.sql'), 'r') as f:
    con.executescript(f.read())
    print("Imported schema from 'schema.sql'")

con.commit()
con.close()

print('To load the data into the new database, execute the following after starting the API:')
print('~$ for user in db/data/user_*.json; do')
print('>   curl -X POST -H "Content-Type: application/json" -d @$user http://localhost:5000/api/user/new')
print('> done')
print('')
