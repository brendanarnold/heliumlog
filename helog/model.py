from __future__ import with_statement
from helog import app
from contextlib import closing
import sqlite3

# Pulls data from flat files edited by Bob/James
def parse_list_file(filename):
    fh = open(filename, 'r')
    items = [s.strip() for s in fh.readlines() if s.strip() != '']
    items.sort()
    fh.close()
    return items

# Read the files that Bob/James can edit
users = parse_list_file(app.config['USER_LIST_FILENAME'])
transport_dewars = parse_list_file(app.config['TRANSPORT_DEWAR_LIST_FILENAME'])
meters = parse_list_file(app.config['METER_LIST_FILENAME'])
cryostats = parse_list_file(app.config['CRYOSTAT_LIST_FILENAME'])


# A function to access the data base
def connect_db():
    return sqlite3.connect(app.config['DB_FILENAME'])

# A function to create the database
def create_db():
    '''
    Perform the following to create the db

    >>> from helog.model import create_db
    >>> create_db()
    '''
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
