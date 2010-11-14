from __future__ import with_statement
from helog import app
from flask import g
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
    return sqlite3.connect(app.config['DB_FILENAME'], \
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

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

# A function to easily query the db
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


# A function to enter a new transfer
def add_transfer(t):
    g.db.execute('insert into entries (user, meter, meter_before, ' \
        + 'meter_after, transport_dewar, transport_dewar_before, ' \
        + 'transport_dewar_after, cryostat, cryostat_before, ' \
        + 'cryostat_after, time) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ' \
        + '?, ?)', [t['user'], t['meter'], t['meter_before'], \
        t['meter_after'], t['transport_dewar'], \
        t['transport_dewar_before'], \
        t['transport_dewar_after'], \
        t['cryostat'], t['cryostat_before'], \
        t['cryostat_after'], t['time']])
    g.db.commit()

# A helper function to retrieve transfers
def get_transfers(restrict_by, id):
    if restrict_by == 'user':
        val = users[id]
        transfers = query_db("select * from entries where user = ? order by time", [val])
    if restrict_by == 'meter': 
        val = meters[id]
        transfers = query_db("select * from entries where meter = ? order by time", [val])
    if restrict_by == 'transport_dewar': 
        val = transport_dewars[id]
        transfers = query_db("select * from entries where transport_dewar = ? order by time", [val])
    if restrict_by == 'cryostat': 
        val = cryostats[id]
        transfers = query_db("select * from entries where cryostat = ? order by time", [val])
    return transfers
        
