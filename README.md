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

1. Open two terminal windows -- one for the app console and one for the api.
2. In the first terminal, enter `yarn start` to start the react app on port 3000.
3. In the second terminal, enter `yarn start-api` to start the flask api on port 5000.
