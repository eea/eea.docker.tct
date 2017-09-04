FROM python:2-alpine3.6
MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV PROJ_DIR=/var/local/tct/

RUN runDeps="gcc musl-dev gettext postgresql-dev netcat-openbsd libressl-dev openldap-dev" \
    && apk add --no-cache $runDeps

RUN apk add --no-cache --virtual .build-deps \
        gcc musl-dev postgresql-dev libressl-dev \
    && apk add --no-cache \
        gettext netcat-openbsd openldap-dev \
    && mkdir -p $PROJ_DIR

# Add requirements.txt before rest of repo for caching
COPY requirements.txt $PROJ_DIR
WORKDIR $PROJ_DIR

RUN pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . $PROJ_DIR

# Fixes bug that is being thrown by postgres interacting with ldap (see http://stackoverflow.com/questions/38740631/need-to-pre-import-module-to-avoid-error)
RUN echo -e "--- config.original.py\n+++ config.py\n@@ -104,6 +104,7 @@\n         else:\n             try:\n                 # If this works, the app module specifies an app config class.\n+                if entry == 'django.contrib.postgres': import ldap\n                 entry = module.default_app_config\n             except AttributeError:\n                 # Otherwise, it simply uses the default app config class." > /tmp/config.py.patch
RUN cd /usr/local/lib/python2.7/site-packages/django/apps/ && patch < /tmp/config.py.patch
RUN echo -e "--- settings.original.py\n+++ settings.py\n@@ -1,5 +1,6 @@\n import os\n import sys\n+import ldap\n from getenv import env\n from django.utils.translation import ugettext_lazy as _\n \n" > /tmp/settings.py.patch
RUN cd /var/local/tct/tct/ && patch < /tmp/settings.py.patch

RUN python manage.py makemessages \
    && python manage.py compilemessages \
    && python manage.py collectstatic --noinput

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["run"]
