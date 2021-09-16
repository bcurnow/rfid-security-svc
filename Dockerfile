from python:3 as dev_image

ARG USER_ID=0
ARG GROUP_ID=0
ARG INPUT_GROUP_ID=9999
ARG FLASK_ENV=development
ARG FLASK_DEBUG=1

# Don't attempt to set the flask user to the root user (uid=0) or group (gid=0)
RUN if [ ${USER_ID:-0} -eq 0 ] || [ ${GROUP_ID:-0} -eq 0 ]; then \
        groupadd flask \
        && useradd -g flask flask \
        ;\
    else \
        groupadd -g ${GROUP_ID} flask \
        && useradd -l -u ${USER_ID} -g flask flask \
        ;\
    fi \
    && install -d -m 0755 -o flask -g flask /home/flask \
    && mkdir -p /etc/sudoers.d  \
    && echo "flask ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/flask-all-nopasswd

# Add the input group
RUN groupadd -g ${INPUT_GROUP_ID} input \
    && usermod -a -G input flask

RUN apt-get update && apt-get -y install --no-install-recommends \
      less \
      sudo \
      vim \
 && rm -rf /var/lib/apt/lists/*

COPY ./docker-files/home/.* /home/flask/

COPY ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

ENV FLASK_APP=rfidsecuritysvc
ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_DEBUG=${FLASK_DEBUG}

WORKDIR /rfid-security-svc

RUN mkdir /rfid-db && chown flask:flask /rfid-db && chmod 750 /rfid-db
VOLUME /rfid-db

EXPOSE 5000

USER flask

CMD ["flask", "run", "--host", "0.0.0.0"]

from dev_image as packager

WORKDIR /package

COPY --chown=flask:flask . .

RUN pip install --no-warn-script-location build
RUN python -m build --wheel

from python:3 as prod_build

ARG USER=rfidsecuritysvc
ARG GROUP=${USER}
ARG VERSION=1.0.0

ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

RUN groupadd ${GROUP} \
 && useradd -g ${USER} ${GROUP} \
 && install -d -m 0755 -o ${USER} -g ${GROUP} /home/${USER}

RUN apt-get update && apt-get -y install --no-install-recommends gunicorn3

USER ${USER}:${GROUP}

COPY --from=packager --chown=${USER}:${GROUP} /package/dist/rfidsecuritysvc-${VERSION}-py3-none-any.whl /tmp

RUN pip install --no-warn-script-location /tmp/rfidsecuritysvc-${VERSION}-py3-none-any.whl && rm -rf /tmp/rfidsecuritysvc-${VERSION}-py3-none-any.whl

EXPOSE 5000

CMD ["/usr/bin/gunicorn3", "--bind", "0.0.0.0:5000", "--preload", "--workers", "2", "--umask", "007", "rfidsecuritysvc:create_app()"]
