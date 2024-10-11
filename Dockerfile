FROM ubuntu:24.04

WORKDIR /app

COPY . .

ENV PYNGUIN_DANGER_AWARE=1

RUN apt update && \
    apt install -y curl && \
    apt install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt install -y python3.10 && \
    apt install -y python3.10-dev && \
    apt install -y python3.10-distutils &&\
    apt install -y nodejs && \
    apt install -y npm && \
    apt install -y sqlite3 && \
    apt install -y sshpass && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    pip3 install -r requirements.txt
