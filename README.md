# gradly

## Environment Setup

1. Install Yarn
    ```shell
    $ brew install yarn
    $ yarn add react-scripts  # maybe unnecessary, I had to do this
    ```
2. Create API venv
    ```shell
    $ cd app/api
    $ python3 -m venv venv
    $ pip install -r requirements.txt
    ```

## Running the App

1. Open two terminal windows -- one for the app console and one for the api. Navigate to the `gradly/app` directory in both.
2. In the first terminal, enter `yarn start-api` to start the flask api on port 5000.
1. In the second terminal, enter `yarn start` to start the react app on port 3000.

Your browser should automatically open to `localhost:3000`. You may also use `curl` to interact with the API directly.

## Managing the database

While the frontend does provide CRUD functionality, it is focused on the meta-entity of a human user, rather than the
DB entities which actually make up the relations. Thus, cleaning up extraneous entries or updating the schema must be
done with external tools.

### Editing the database directly

Since the SQLite database is just a file with no server, it is possible to open it in several applications and make edits
on the fly. If you need to edit the database, you may open `gradly/app/db/app.db` in a SQLite viewer of your choice. On
macOS, "DB Browser for SQLite" comes preinstalled.

### Modifying the schema

If it becomes necessary to modify the database schema, you may do so by editing the `db/schema.sql` file. This is not
a live file, meaning you will have to manually edit the database to reflect your changes. If the change is simple, like
updating or adding a single table, you may use the Flask shell to execute the appropriate update commands directly on
the existing database.

```
cd app/api
source venv/bin/activate
flask shell
>>> con.execute('begin')
>>> con.execute('...SQL query here...')
>>> con.commit()
>>> exit
```

For more substantial changes, you may wish to instead nuke the entire database and start from scratch. The `db/bootstrap.py`
script is provided to remove the existing database file and create a new one with the currently defined `schema.sql` file.
Note that any open connections to the database will become readonly when the file is deleted, so you will need to restart
the API and close/reopen any DB browsers to continue interacting with the new database.

If you have significant data stored in the current database, you may wish to back it up. If the updated schema is backwards
compatible with the old one, you may be able to use the Flask shell to run `con.iterdump()` which generates a series of SQL
commands to restore the database. If the schemas are not compatible, you will have to export the data using the JSON schema
defined by the API. The following Python code will generate JSON documents for each current user.

```python
import json
import requests
import sqlite3

con = sqlite3.connect('db/app.db')

users = con.execute('SELECT id FROM user').fetchall()
userIDs = map(lambda u: u['id'], users)

for id in userIDs:
    userInfo = requests.get(f'localhost:5000/api/user/{id}').json()
    with open(f'db/data/dump_user_{id}', w) as f:
        f.write(json.dumps(userInfo)) # optionally include indent=2 to pretty print
```

The bootstrap script provides printed instructions for loading bulk JSON data into a fresh database, just adjust the filename
glob accordingly.

**Note:** the DB file would usually not be under version control. We wanted to ensure an easily reproducible testing
and demonstration environment so we committed a version of the DB with 20 seed users. We recommend against committing
changes to this DB in your project.

## Testing

### CRUD

1. start up the api server with `yarn start-api` from within the `/app` directory.
2. Add a new user: `cat db/data/user_<name>.json | curl -H "Content-Type: application/json" -d @- http://localhost:5000/api/user/new`, where `<name>` is some identifier. Note the userID returned by the server.
3. Read the user's data: `curl http://localhost:5000/api/user/<id>`. Optionally, open the database file (`db/app.db`) in a database viewer (DB Browser for SQLite on macOS) to verify the data integrity.
4. [Optional] Add an identical user so the update is easier to see in the DB browser.
5. Update the user information: `cat db/data/user_<name>_update.json | curl -H "Content-Type: application/json" -d @- http://localhost:5000/api/user/<id>`.

    - Note the format of the update JSON document. The schema is the same as the new user document, but only attributes which are included will be changed.
    - To leave a value unchanged, simply do not include it in the update file.
    - To remove a value, provide `null` for that parameter.
    - To remove an entity (object), set `delete` to `true`.

6. After verifying that the update took place, we may delete the user(s): `curl -X DELETE http://localhost:5000/api/user/<id>`.

    - Note that deleting a user only deletes the relationships associated with the user, but not the entities on the other end of the relationships.
    - Courses, Universities, Positions, and Employers will persist a user deletion.
    - Graduations, Enrollments, and Experience will automatically be removed when the user is deleted.

## Making API Changes

Most API changes will just be straightforward edits of the files in the `/app/api` directory. There are a few caveats though.

- Executing the api server using `yarn start-api` will automatically invoke the virtualenv. However, you will need to activate it yourself to install new packages or run the files directly with flask.
  1. From the `/app/api` directory, execute `source venv/bin/activate` to load the virtual environment.
  2. You can now use `flask run`, `pip install`, etc. relative to the api environment.
- **IMPORTANT** If you `pip install` anything, be sure to update the `requirements.txt` so everyone's local environment stays up to date.
- If new packages have been installed, you can update your local environment by running `pip install -r requirements.txt` again from within the `/app/api` folder.
