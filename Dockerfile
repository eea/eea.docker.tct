FROM python:2.7-slim
RUN apt-get -y update
RUN apt-get -y install python2.7-dev python-setuptools python-pip
RUN apt-get -y install libldap2-dev libsasl2-dev libmysqlclient-dev libxml2-dev libxslt1-dev

# add the code to the image
RUN mkdir /nbsap
WORKDIR /nbsap
ADD . /nbsap

# install requirements
RUN pip install -r requirements.txt
RUN pip install -U distribute
RUN pip install -e .

# apply migrations & fixtures
CMD bash -c "python instance/manage.py syncdb && python instance/manage.py load_fixtures"
