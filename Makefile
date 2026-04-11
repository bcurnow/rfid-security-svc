SHELL := /bin/bash
ROOT_DIR := $(CURDIR)
IMAGE_NAME := $(notdir $(CURDIR))
PID_FILE := $(ROOT_DIR)/rfidsecuritysvc.pid
LOG_FILE := $(ROOT_DIR)/rfidsecuritysvc.log
INPUT_GROUP_ID := $(shell getent group input | cut -d: -f3)
PRODUCTION_PLATFORM := linux/arm/v6

.PHONY: help build build-prod docker docker-prod generate-key reset run run-background stop test coverage lint format

help:
	@printf "Usage:\n"
	@printf "  make build                Build the development Docker image\n"
	@printf "  make build-prod           Build the production Docker image\n"
	@printf "  make docker               Run the development image in an interactive shell\n"
	@printf "  make docker-prod ARGS=... Run the production image\n"
	@printf "  make generate-key         Generate a new API key\n"
	@printf "  make reset                Delete the SQLite database\n"
	@printf "  make run                  Start API server in the foreground\n"
	@printf "  make run-background       Stop and start API server in the backgroun, then tail the logs\n"
	@printf "  make tail                 Tail API server logs\n"
	@printf "  make run-testing          Reset database, stop and start API server in the background, then tail the logs\n"
	@printf "  make stop                 Stop API server started by make run\n"
	@printf "  make test ARGS=...        Run tests with pytest\n"
	@printf "  make coverage             Run tests with coverage and prints report\n"
	@printf "  make lint                 Run ruff to check and fix linting issues\n"
	@printf "  make format               Run ruff to format code\n"

build:
	docker image build \
	  --target dev_image \
	  --build-arg USER_ID=$(shell id -u) \
	  --build-arg GROUP_ID=$(shell id -g) \
	  --build-arg INPUT_GROUP_ID=$(INPUT_GROUP_ID) \
	  --tag $(IMAGE_NAME):latest \
	  $(ROOT_DIR)

build-prod:
	docker buildx build \
	  --platform $(PRODUCTION_PLATFORM) \
	  --target prod_build \
	  --tag $(IMAGE_NAME):production \
	  $(ROOT_DIR)

docker:
	@mkdir -p $(ROOT_DIR)/rfid-db
	@if [[ -e /dev/input/rfid && -c /dev/input/rfid ]]; then \
	  docker run --rm --name rfid-security-svc -it -p 5000:5000 --mount src=$(ROOT_DIR)/rfid-db,target=/rfid-db,type=bind--mount src="$(ROOT_DIR)",target=/rfid-security-svc,type=bind --device=/dev/input/rfid:/dev/input/rfid:r $(IMAGE_NAME):latest /bin/bash; \
	else \
	  echo "Did not find /dev/input/rfid, skipping --device"; \
	  docker run --rm --name rfid-security-svc -it -p 5000:5000 --mount src=$(ROOT_DIR)/rfid-db,target=/rfid-db,type=bind --mount src="$(ROOT_DIR)",target=/rfid-security-svc,type=bind $(IMAGE_NAME):latest /bin/bash; \
	fi

docker-prod:
	@mkdir -p $(ROOT_DIR)/rfid-db
	docker run --rm --name rfid-security-svc -p 5000:5000 --mount src=$(ROOT_DIR)/rfid-db,target=/rfid-db,type=bind $(IMAGE_NAME):production $(ARGS)

generate-key:
	@rfidsecuritysvc-genkey

reset:
	rm $(ROOT_DIR)/rfid-db/*

run:
	uvicorn rfidsecuritysvc:app --host 0.0.0.0 --port 5000 --reload --lifespan on --no-server-header --log-level debug

run-background:
	@if [ -f "$(PID_FILE)" ]; then \
	  echo "API server is currently running, please use make stop or cleanup $(PID_FILE)" >&2; \
	  exit 1; \
	fi; \
	uvicorn rfidsecuritysvc:app --host 0.0.0.0 --port 5000 --reload --lifespan on --no-server-header --log-level debug> "$(LOG_FILE)" 2>&1 & \
	pid=$$!; \
	echo $$pid > "$(PID_FILE)"; \
	echo "API server is running under pid $$pid, logs are located at $(LOG_FILE)" \

tail:
	@pid=$$(cat "$(PID_FILE)"); \
	tail -F -n +1 --pid=$$pid rfidsecuritysvc.log

run-testing: reset stop run-background tail
	
stop:
	@if [ -f "$(PID_FILE)" ]; then \
	  pid=$$(cat "$(PID_FILE)"); \
	  if ps -p $$pid -o cmd | grep -q uvicorn; then \
	    echo "Killing $$pid..."; \
	    kill $$pid; \
	    sleep 1; \
	    rm "$(PID_FILE)"; \
	  else \
	    echo "Pid $$pid is not a uvicorn process, cleaning up $(PID_FILE)" >&2; \
	    rm "$(PID_FILE)"; \
	  fi; \
	else \
	  echo "API server is not currently running, can't find $(PID_FILE)" >&2; \
	fi

.test-install:
	@pip list | grep rfidsecuritysvc | grep "/rfid-security-svc" >/dev/null; \
	if [ $$? -ne 0 ]; then \
	  pip --disable-pip-version-check --no-cache-dir install -e .; \
	fi


test: .test-install
	pytest --import-mode=importlib $(ARGS)

coverage: .test-install
	coverage run -m pytest --import-mode=importlib
	coverage report

lint:
	ruff check . --fix

format:
	ruff format .