# rfid-security-svc
Python3, Flask and Connexion backend service enabling management of RFID media, permissions and associations

# Docker container

This application is designed to run inside a Docker container. That gives you a clean environment for the application and avoids cluttering your system with local dependencies or virtual environments.

Use `make` targets instead of shell scripts for the same commands:

  make build
  make build-prod
  make docker
  make flask ARGS="..."
  make prod ARGS="..."
  make run
  make stop
  make testing

## Development container

Build the development image:

  make build

Run the development container interactively:

  make docker

This exposes port `5000` and mounts the repository into the container. If `/dev/input/rfid` exists, it is also forwarded into the container.

Inside the container, use `make flask ARGS="..."` to invoke Flask with the correct environment.

## Running Flask locally

Start the development Flask server in the background:

  make run

This writes a PID file at `flask.pid` and logs to `flask.log`.

Stop the background Flask process:

  make stop

## Production image

Build the production image:

  make build-prod

Run the production image:

  make prod ARGS="..."

# Testing

Install the package for test execution:

  pip install -e .

Run the test suite:

  pytest --import-mode=importlib

Run tests with coverage:

  coverage run -m pytest --import-mode=importlib
  coverage report

# First time setup

Before you run the API, initialize the database and create an API key:

  make init
  make flask ARGS="config create RFID_DEVICE <device name>"

The `make init` target will run the database initialization and generate a new API key into `test.apikey`.

Use the device path for your system, typically `/dev/input/rfid`.

Then start the API:

  make run
