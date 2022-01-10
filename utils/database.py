from tinydb import TinyDB
import pickledb

stats_db = pickledb.load('../data/stats.db', True)
db = TinyDB('../data/db.json')


def update_req_count():
    stats_db.append('requests_made', 1)
    stats_db.set('requests_made', stats_db.get('requests_made'))


def get_current_req_count():
    return int(stats_db.get('requests_made'))


def log_request(message, arguments) -> None:
    args = dict(arguments.__dict__.items())
    args2 = args.copy()
    for k, v in args2.items():
        if not v:
            args.pop(k)
    db.insert({'MessageID': str(message.id), 'NumbRequest': get_current_req_count() + 1, 'author': str(message.author),
               'Args': args})
