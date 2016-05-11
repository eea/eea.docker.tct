FROM python:2.7-slim
RUN apt-get -y update
RUN apt-get -y install python2.7-dev python-setuptools python-pip
RUN apt-get -y install libldap2-dev libsasl2-dev libmysqlclient-dev libxml2-dev libxslt1-dev
RUN apt-get -y install git

# add the code to the image
RUN mkdir /nbsap
WORKDIR /nbsap
ADD . /nbsap

# install requirements
RUN pip install -r requirements.txt
RUN pip install -e .

WORKDIR /usr/local/lib/python2.7/site-packages/django
CMD django-admin.py makemessages -a
CMD django-admin.py compilemessages

WORKDIR /nbsap

