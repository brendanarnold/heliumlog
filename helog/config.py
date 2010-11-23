import os
from ConfigParser import SafeConfigParser

cf = SafeConfigParser()
cf.read(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))

deploy = cf.get('main', 'DEPLOY')

SECRET_KEY = cf.get(deploy, 'SECRET_KEY')
DEBUG = cf.get(deploy, 'DEBUG')
DB_FILENAME = cf.get(deploy, 'DB_FILENAME')
USER_LIST_FILENAME = cf.get(deploy, 'USER_LIST_FILENAME')
TRANSPORT_DEWAR_LIST_FILENAME = cf.get(deploy, 'TRANSPORT_DEWAR_LIST_FILENAME')
METER_LIST_FILENAME = cf.get(deploy, 'METER_LIST_FILENAME')
CRYOSTAT_LIST_FILENAME = cf.get(deploy, 'CRYOSTAT_LIST_FILENAME')
