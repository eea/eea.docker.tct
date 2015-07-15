#start from an ubuntu image
FROM ubuntu:14.04
RUN apt-get -y update
RUN apt-get -y install python2.7 python2.7-dev python-setuptools python-pip
RUN apt-get -y install libldap2-dev libsasl2-dev libmysqlclient-dev libxml2-dev libxslt1-dev

#add the code to the image
RUN mkdir /nbsap
WORKDIR /nbsap
ADD . /nbsap
ADD src/nbsap/settings.py.docker /nbsap/instance/settings.py

#install the requirements
RUN pip install -r requirements-dev.txt
RUN pip install -U distribute
RUN pip install -e .

#default cmd
EXPOSE ${APP_PORT}
CMD python instance/manage.py runserver 0.0.0.0:${APP_PORT}
