from python:3

ARG USER_ID
ARG GROUP_ID

RUN if [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    groupadd -g ${GROUP_ID} flask && \
    useradd -l -u ${USER_ID} -g flask flask && \
    install -d -m 0755 -o flask -g flask /home/flask && \
    mkdir -p /etc/sudoers.d && \
    echo "flask ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/flask-all-nopasswd && \
    echo "PATH=.:\${PATH}\nset -o vi" > /home/flask/.bashrc \
;fi

COPY ./docker-files/home/.* /home/flask/
COPY ./requirements.txt /var/tmp

RUN apt-get update && \
    apt-get -y install --no-install-recommends vim sudo less && \
    pip install -r /var/tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

USER flask

WORKDIR /rfid-security-svc

EXPOSE 5000
