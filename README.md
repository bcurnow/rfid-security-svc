# rfid-security-svc
Python3, Flask and Connexion backend service enabling management of RFID media, permissions and associations

# Docker container

This application is designed to run insted a Docker container. This ensures that we have a clean environment for the application to run in and you won't clutter your actual system. This means we don't need to worry about virtual environemnts because we have a clean systems that's just for this application.

You first need to build the container, use the command `build.ssh`. This will capture the currently logged in user and configure a new container with a `flask` user that maps to the same uid and gid as that user. This is important as the current directly will be mounted inside the container. Without this mapping, any changes that you try to make will happen using the uid and gid of the `flask` user in the container but this may not map to a uid and gid on your system. This will screw up the permissions on things and make it very inconvenient.

Once the container has built, you can run it using the `docker.sh` script. This script will launch the container, expose port 5000 from the contain as port 5000 on your system and mount the current working directly inside the container. You should now be sitting at a prompt that indicates you are logged in as the `flask` user.

Once in the container, there is a `flask.sh` script that wraps the standard `flask` command and provides all the necessary environment variables. `flask.shs` can be used to execute your command line commands and is a replacement for `flask` within the container.

If you'd like to run the application, use the `run.sh` script. This will startup Flask in development mode, create a pid file and a redirect logs to flask.log.

To stop Flask, use the `stop.sh` script, this will look for the pid file created by `run.sh`, validate the process is Flask and stop it.

# Testing

When you're ready to test your application, you'll need to first install it with pip: `pip install -e .`. Please keep in mind that, since you're in a Docker container, if you exit, this installation will be cleared so you'll need to install again. This is one of the main advantages of this setup, any changes you make in the container to the working directory stay. Any changes you make to the system get reset.

Once you've installed with pip, you can run the tests with `pytest --import-mode=importlib`

You can also run using coverage.py by using `coverage run -m pytest --import-mode=importlib`

Once you're doing running, you can get a coverage report with `coverage report`

# First time setup

Before you can run Flask and actually execute the APIs, you'll need to setup the database, run the following commands:
* `scripts/flask.sh db init` - When prompted, answer `y` to setup the tables.
* `scripts/flask.sh auth generate-api-key` - When prompted, answer `y` to invalidated the old key (there is no old key, you just created an empty DB). It will be helpful to record the value printed by this command as it's not retrievable again but you need it to authorize in the Swagger UI.
* `scripts/flask.sh config create RFID_DEVICE <device name>` - This is likely /dev/input/rfid but if your setup has a different device name, replace it here. This tells the API what device to read from.

Now you can run the API with `scripts/run.sh`.
