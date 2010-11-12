from helog.config import *

def parse_list_file(filename):
    fh = open(filename, 'r')
    items = [s.strip() for s in fh.readlines() if s.strip() != '']
    items.sort()
    fh.close()
    return items

# Read the files that Bob/James can edit
users = parse_list_file(USER_LIST_FILENAME)
transport_dewars = parse_list_file(TRANSPORT_DEWAR_LIST_FILENAME)
meters = parse_list_file(METER_LIST_FILENAME)
cryostats = parse_list_file(CRYOSTAT_LIST_FILENAME)


