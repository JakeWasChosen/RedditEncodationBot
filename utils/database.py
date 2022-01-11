from time import time

from tinydb import TinyDB
import pickledb
from tinydb.table import Table

stats_db = pickledb.load('data/stats.db', True)
db = TinyDB('data/db.json')
reqdb: Table = db.table('requests')


def update_req_count():
    stats_db.append('requests_made', 1)

def get_current_req_count():
    return int(stats_db.get('requests_made'))

def log_request(message, arguments) -> None:
    args = dict(arguments.__dict__.items())
    args2 = args.copy()
    for k, v in args2.items():
        if not v:
            args.pop(k)
    reqdb.insert({'MessageID': str(message.id), 'time': time(), 'NumbRequest': get_current_req_count() + 1,
                  'author': str(message.author),
                  'Args': args})

def request(message, arguments):
    """ general calling function """
    update_req_count()
    log_request(message, arguments)
