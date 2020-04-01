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
2. In the first terminal, enter `yarn start` to start the react app on port 3000.
3. In the second terminal, enter `yarn start-api` to start the flask api on port 5000.

## Making API Changes

Most API changes will just be straightforward edits of the files in the `/app/api` directory. There are a few caveats though.

- Executing the api server using `yarn start-api` will automatically invoke the virtualenv. However, you will need to activate it yourself to install new packages or run the files directly with flask.
  1. From the `/app/api` directory, execute `source venv/bin/activate` to load the virtual environment.
  2. You can now use `flask run`, `pip install`, etc. relative to the api environment.
- **IMPORTANT** If you `pip install` anything, be sure to update the `requirements.txt` so everyone's local environment stays up to date.
- If new packages have been installed, you can update your local environment by running `pip install -r requirements.txt` again from within the `/app/api` folder.
