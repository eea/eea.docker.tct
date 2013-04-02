git clone git@mojito.edw.ro:nbsap.git nbsap
virtualenv -p /usr/local/bin/python2.7 . --distribute
pip install -U distribute
pip install -r requirements.txt 
pip install -e .