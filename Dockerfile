FROM python:2.7-slim

MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV PROJ_DIR=/var/local/tct

RUN runDeps="build-essential git vim libmysqlclient-dev libldap2-dev libsasl2-dev" \
    && apt-get -y update \
    && apt-get install -y --no-install-recommends $runDeps \
    && rm -vrf /var/lib/apt/lists/*

RUN mkdir -p $PROJ_DIR
COPY . $PROJ_DIR
WORKDIR $PROJ_DIR

#RUN apt-get -y install python2.7-dev python-setuptools python-pip

RUN pip install -r requirements.txt

CMD "cat"
