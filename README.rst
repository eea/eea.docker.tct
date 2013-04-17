git clone git@mojito.edw.ro:nbsap.git nbsap
virtualenv -p /usr/local/bin/python2.7 . --distribute
apt-get install mysql-server
apt-get install libmysqlclient-dev
apt-get install python-dev
pip install mysql-python
pip install -U distribute
pip install -r requirements.txt
pip install -e .
