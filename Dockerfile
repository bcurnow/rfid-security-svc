from python:3

ARG USER_ID
ARG GROUP_ID

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
    && echo "flask ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/flask-all-nopasswd \
    && echo "PATH=.:\${PATH}\nset -o vi" > /home/flask/.bashrc

COPY ./docker-files/home/.* /home/flask/
COPY ./requirements.txt /var/tmp

RUN apt-get update && \
    apt-get -y install --no-install-recommends vim sudo less && \
    pip install -r /var/tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/*

USER flask

WORKDIR /rfid-security-svc

EXPOSE 5000
