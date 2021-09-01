from python:3

ARG USER_ID
ARG GROUP_ID
ARG INPUT_GROUP_ID
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
