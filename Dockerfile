FROM python:3 AS dev_image

ARG USER_ID=0
ARG GROUP_ID=0
ARG INPUT_GROUP_ID=9999

# Don't attempt to set the rfidsecsvc user to the root user (uid=0) or group (gid=0)
RUN if [ ${USER_ID:-0} -eq 0 ] || [ ${GROUP_ID:-0} -eq 0 ]; then \
        groupadd rfidsecsvc \
        && useradd -g rfidsecsvc rfidsecsvc \
        ;\
    else \
        groupadd -g ${GROUP_ID} rfidsecsvc \
        && useradd -l -u ${USER_ID} -g rfidsecsvc rfidsecsvc \
        ;\
    fi \
    && install -d -m 0755 -o rfidsecsvc -g rfidsecsvc /home/rfidsecsvc \
    && mkdir -p /etc/sudoers.d  \
    && echo "rfidsecsvc ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/rfidsecsvc-all-nopasswd

# Add the input group
RUN groupadd -g ${INPUT_GROUP_ID} input \
    && usermod -a -G input rfidsecsvc

RUN apt-get update && apt-get -y install --no-install-recommends \
      less \
      sudo \
      vim \
 && rm -rf /var/lib/apt/lists/*

COPY ./docker-files/home/.* /home/rfidsecsvc/

COPY ./requirements.txt /tmp

RUN pip3 --disable-pip-version-check install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /rfid-security-svc

RUN mkdir /rfid-db && chown rfidsecsvc:rfidsecsvc /rfid-db && chmod 750 /rfid-db
VOLUME /rfid-db

EXPOSE 5000

USER rfidsecsvc

FROM python:3 AS packager

USER root
WORKDIR /package

# Install the build command
RUN pip3 --disable-pip-version-check install build

COPY  LICENSE .
COPY  MANIFEST.in .
COPY  README.md .
COPY  rfidsecuritysvc ./rfidsecuritysvc/
COPY  setup.cfg .
COPY  setup.py .

# Build and make sure to include the wheel
RUN python3 -m build --wheel

FROM python:3 AS prod_build

ARG USER=rfidsecuritysvc
ARG GROUP=${USER}
ARG VERSION=2.0.0

RUN groupadd ${GROUP} \
 && useradd -g ${USER} ${GROUP} \
 && install -d -m 0755 -o ${USER} -g ${GROUP} /home/${USER}

COPY --from=packager --chown=${USER}:${GROUP} /package/dist/rfidsecuritysvc-${VERSION}-py3-none-any.whl /tmp

RUN pip3 --disable-pip-version-check install /tmp/rfidsecuritysvc-${VERSION}-py3-none-any.whl && rm -rf /tmp/rfidsecuritysvc-${VERSION}-py3-none-any.whl

# Create the database volume
RUN mkdir /rfid-db && chown ${USER}:${GROUP} /rfid-db && chmod 750 /rfid-db
VOLUME /rfid-db

# Create a directory for the application
RUN mkdir /app && chown ${USER}:${GROUP} /app && chmod 750 /app

# Create a diretory for the default sounds
RUN mkdir /app/sounds && chown ${USER}:${GROUP} /app/sounds && chmod 750 /app/sounds

COPY --chown=${USER}:${GROUP} docker-files/sounds/*.wav /app/sounds/

EXPOSE 5000

USER ${USER}:${GROUP}

ENTRYPOINT ["uvicorn"]
CMD ["rfidsecuritysvc:app", "--host", "0.0.0.0", "--port", "5000", "--lifespan", "on", "--no-server-header", "--workers", "2"]