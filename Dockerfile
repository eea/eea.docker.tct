FROM python:2-alpine3.6
MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV PROJ_DIR=/var/local/tct

RUN runDeps="gcc git musl-dev gettext postgresql-client postgresql-dev netcat-openbsd libressl-dev openldap-dev" \
    && apk add --no-cache $runDeps

RUN mkdir -p $PROJ_DIR
COPY . $PROJ_DIR
WORKDIR $PROJ_DIR

RUN pip install -r requirements.txt

# Fixes bug that is being thrown by postgres interacting with ldap (see http://stackoverflow.com/questions/38740631/need-to-pre-import-module-to-avoid-error)
RUN echo -e "--- /usr/local/lib/python2.7/site-packages/django/apps/config.original.py\n+++ /usr/local/lib/python2.7/site-packages/django/apps/config.py\n@@ -104,6 +104,7 @@\n         else:\n             try:\n                 # If this works, the app module specifies an app config class.\n+                if entry == 'django.contrib.postgres': import ldap\n                 entry = module.default_app_config\n             except AttributeError:\n                 # Otherwise, it simply uses the default app config class." > /tmp/config.py.patch
RUN cd /usr/local/lib/python2.7/site-packages/django/apps/ && patch config.py /tmp/config.py.patch

RUN python manage.py makemessages
RUN python manage.py compilemessages
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["run"]
