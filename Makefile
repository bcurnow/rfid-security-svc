SHELL := /bin/bash
ROOT_DIR := $(CURDIR)
IMAGE_NAME := $(notdir $(CURDIR))
PID_FILE := $(ROOT_DIR)/flask.pid
LOG_FILE := $(ROOT_DIR)/flask.log
INPUT_GROUP_ID := $(shell getent group input | cut -d: -f3)

.PHONY: help build build-prod docker flask prod run stop testing init

help:
	@printf "Usage:\n"
	@printf "  make build          Build the development Docker image\n"
	@printf "  make build-prod     Build the production Docker image\n"
	@printf "  make docker         Run the development image in an interactive shell\n"
	@printf "  make flask ARGS=...  Run flask with the given arguments\n"
	@printf "  make prod ARGS=...   Run the production image\n"
	@printf "  make run            Start Flask in the background\n"
	@printf "  make stop           Stop Flask started by make run\n"
	@printf "  make testing        Stop and start Flask, then tail the logs\n"
	@printf "  make init           Initialize the database and generate an API key\n"

build:
	docker image build \
	  --target dev_image \
	  --build-arg USER_ID=$(shell id -u) \
	  --build-arg GROUP_ID=$(shell id -g) \
	  --build-arg INPUT_GROUP_ID=$(INPUT_GROUP_ID) \
	  -t $(IMAGE_NAME):latest \
	  $(ROOT_DIR)

build-prod:
	docker image build \
	  --platform linux/arm/v6 \
	  -t $(IMAGE_NAME):production \
	  $(ROOT_DIR)

docker:
	@if [[ -e /dev/input/rfid && -c /dev/input/rfid ]]; then \
	  docker run -it -p 5000:5000 --mount src=rfid-db,target=/rfid-db --mount src="$(ROOT_DIR)",target=/rfid-security-svc,type=bind --device=/dev/input/rfid:/dev/input/rfid:r $(IMAGE_NAME):latest /bin/bash; \
	else \
	  echo "Did not find /dev/input/rfid, skipping --device"; \
	  docker run -it -p 5000:5000 --mount src=rfid-db,target=/rfid-db --mount src="$(ROOT_DIR)",target=/rfid-security-svc,type=bind $(IMAGE_NAME):latest /bin/bash; \
	fi

flask:
	FLASK_APP=rfidsecuritysvc FLASK_ENV=development flask $(ARGS)

prod:
	docker run -p 5000:5000 --mount src=rfid-db,target=/rfid-db $(IMAGE_NAME):production $(ARGS)

init:
	@FLASK_APP=rfidsecuritysvc FLASK_ENV=development flask db init --yes
	@FLASK_APP=rfidsecuritysvc FLASK_ENV=development flask auth generate-api-key --yes | sed 's/.*\"\(.*\)\".*/\1/' > test.apikey
	@echo "API key written to test.apikey"

run:
	@if [ -f "$(PID_FILE)" ]; then \
	  echo "Flask is currently running, please use make stop or cleanup $(PID_FILE)" >&2; \
	  exit 1; \
	fi; \
	FLASK_APP=rfidsecuritysvc FLASK_ENV=development FLASK_DEBUG=1 flask run --host 0.0.0.0 > "$(LOG_FILE)" 2>&1 & \
	pid=$$!; \
	echo $$pid > "$(PID_FILE)"; \
	echo "Flask is running under pid $$pid, logs are located at $(LOG_FILE)"

stop:
	@if [ -f "$(PID_FILE)" ]; then \
	  pid=$$(cat "$(PID_FILE)"); \
	  if ps -p $$pid -o cmd | grep -q flask; then \
	    echo "Killing $$pid..."; \
	    kill $$pid; \
	    rm "$(PID_FILE)"; \
	  else \
	    echo "Pid $$pid is not a Flask process, cleaning up $(PID_FILE)" >&2; \
	    rm "$(PID_FILE)"; \
	  fi; \
	else \
	  echo "Flask is not currently running, can't find $(PID_FILE)" >&2; \
	fi

testing: stop run
	@cat test.apikey
	@tail -F -n +1 flask.log
