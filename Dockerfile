from python:3

ARG USER_ID
ARG GROUP_ID

RUN if [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    groupadd -g ${GROUP_ID} flask && \
    useradd -l -u ${USER_ID} -g flask flask && \
    install -d -m 0755 -o flask -g flask /home/flask && \
    mkdir -p /etc/sudoers.d && \
    echo "flask ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/flask-all-nopasswd \
;fi

COPY ./requirements.txt /var/tmp
COPY ./.vimrc /home/flask/.vimrc

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install --no-install-recommends vim sudo && \
    pip install -r /var/tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

USER flask

WORKDIR /rfid-security-svc

EXPOSE 5000