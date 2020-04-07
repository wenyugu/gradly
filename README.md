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

## Updating the database

The database schema is defined in `/app/api/models.py` as a series of classes and
objects from the SQLAlchemy Flask extension. In general, each class which extends
`db.Model` represents a table. One-to-many relationships are encoded using
foreign keys and `relationships`, which are a high level abstraction of the
reverse foreign key (basically an automatic `SELECT * FROM x WHERE foreignkey = id`). Many-to-many relationships are encoded in `db.Table` objects, at the
recommendation of [the extension authors](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/). These tables contain foreign keys
linking the two entities, as well as some additional attributes.

The database schema can be modified using the Flask-Migrate extension, which
tracks versions of the schema. To create the database for the first time:

1. Ensure the database directory is present. The flask tools don't attempt to create folders that aren't there. The expected path can be found in `app/api/config.py`
2. Inspect the list of revisions using `flask db history`. This will show the entire history of revisions with their comments. You should be able to identify the one you want (probably the newest).
3. Run `flask db upgrade <revision>` to modify the database file according to the revision scripts. You may want to double check using a SQLite browser (built-in on macOS) as the scripts aren't perfect.
4. If you need to return to an older version, use `flask db downgrade <revision>`.

To update the DB schema, modify the models in `models.py`, then execute `flask db migrate` to generate a new revision file.  **NOTE:** This will not actually modify the database, you must run `upgrade` for your changes to take effect.

#### Errors updating schema

If you encounter errors upgrading the schema, one solution is to enter the flask shell and
drop all tables then recreate them.  This will not attempt to retain any data, so this
might not be a good idea if we have significant amounts of data but no automated way to
ingest it.  Anyway, these are the steps:

1. Enter the flask shell with `flask shell`
2. Drop all the tables: `>>> db.drop_all()`
3. Create the new tables: `>>> db.create_all()`
4. Save the DB: `>>> db.session.commit()`
5. Tell alembic (the flask db engine) that we did something and it should treat the current DB state as the application of all revisions: `flask db stamp head`

### Populating the Database

Currently, there is no initial data in the database. The database file itself is
not under version control due to the indeterminate structure of the binary file.
Thus, as we add new data, we will have to synchronize the database instances
across machines.  The easiest way to do that is probably to nuke the DB and
reload from an external file.

*Note from Eric:* My next step is to add import/export support via CSV or SQL
dump.  SQL dump is easier, but dependent on schema. CSV will take some more
thinking to get right.

The exact process for initialization and data ingestion is still in flux, but
will be worked out soon.


## Running the App

1. Open two terminal windows -- one for the app console and one for the api. Navigate to the `gradly/app` directory in both.
2. In the first terminal, enter `yarn start` to start the react app on port 3000.
3. In the second terminal, enter `yarn start-api` to start the flask api on port 5000.

### Testing

#### CRUD

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
