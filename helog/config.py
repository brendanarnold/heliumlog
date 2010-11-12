import os

PREFIX = r'helog'
USER_LIST_FILENAME = os.path.join(PREFIX, r'users.txt')
TRANSPORT_DEWAR_LIST_FILENAME = os.path.join(PREFIX, r'transport_dewars.txt')
METER_LIST_FILENAME = os.path.join(PREFIX, r'meters.txt')
CRYOSTAT_LIST_FILENAME = os.path.join(PREFIX, r'cryostats.txt')
DB_FILENAME = os.path.join(PREFIX, r'helog.sqlite')

SECRET_KEY = 'development'
DEBUG = True
