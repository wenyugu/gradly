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

1. Open two terminal windows -- one for the app console and one for the api.
2. In the first terminal, enter `yarn start` to start the react app on port 3000.
3. In the second terminal, enter `yarn start-api` to start the flask api on port 5000.
