FROM python:2.7-slim

MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV PROJ_DIR=/var/local/tct

RUN runDeps="gcc git vim gettext libmysqlclient-dev libldap2-dev libsasl2-dev" \
    && apt-get -y update \
    && apt-get install -y --no-install-recommends $runDeps \
    && rm -vrf /var/lib/apt/lists/*

RUN mkdir -p $PROJ_DIR
COPY . $PROJ_DIR
WORKDIR $PROJ_DIR

RUN pip install -r requirements.txt

#CMD django-admin.py makemessages
CMD django-admin.py compilemessages

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["run"]
