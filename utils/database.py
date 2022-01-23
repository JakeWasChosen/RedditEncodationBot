import logging
from functools import lru_cache
from time import time
from typing import Optional

import pickledb
from tinydb import TinyDB, Query
from tinydb.table import Table
from tinydb_smartcache import SmartCacheTable

from utils.exeptions import UserError

TinyDB.table_class = SmartCacheTable
stats_db = pickledb.load("data/stats.db", True)
db = TinyDB("data/db.json")
reqdb: Table = db.table("requests")


def update_req_count():
    stats_db.append("requests_made", 1)


def get_current_req_count():
    return int(stats_db.get("requests_made"))


def log_request(message, arguments) -> None:
    args = dict(arguments.__dict__.items())
    args2 = args.copy()
    for k, v in args2.items():
        if not v:
            args.pop(k)
    reqdb.insert(
        {
            "MessageID": str(message.id),
            "time": time(),
            "NumbRequest": get_current_req_count() + 1,
            "author": str(message.author),
            "Args": args,
        }
    )


def request(message, arguments):
    """general calling function"""
    log_request(message, arguments)
    update_req_count()


class Blacklist:
    def __init__(self):
        self.blacklistDB = TinyDB("data/blacklistDB.json")
        self.SubredditBlacklist = self.blacklistDB.table("Subreddit")
        self.UserBlacklist = self.blacklistDB.table("Users")
        self.log = logging.getLogger("Blacklist")

    def __len__(self):
        """
        Get the total number of blacklisted users/guilds in the default table.
        """
        return len(self.SubredditBlacklist) + len(self.UserBlacklist)

    def add_user(self, user, Reason: str = None):
        if not self.CheckUser(user):
            self.log.info(f"Adding {user} to the Blacklist for {Reason}")
            self.UserBlacklist.insert({"ID": user.name, "Reason": Reason})
        else:
            self.log.info(
                f"Failed to add {user} to the Blacklist Because u/{user.name} is already on it"
            )

    def remove_user(self, user):
        Users = Query()
        self.log.info(f"Removing {user} to the Blacklist")
        self.UserBlacklist.remove(Users.ID == user.name)

    @lru_cache(512)
    def CheckUser(self, user):
        User = Query()
        x = self.UserBlacklist.contains(User.ID == user.name)
        if bool(x):
            return True
        else:
            return False

    @lru_cache(512)
    def CheckUserReason(self, user, text: str = None) -> Optional[bool]:
        if self.CheckUser(user):
            User = Query()
            y = self.UserBlacklist.get(User.ID == user.name)
            print(y)
            if y.get("Reason") == text:
                return True
        else:
            return UserError("User isn't Blacklisted")

    @lru_cache(512)
    def CheckSubreddit(self, subreddit):
        if subreddit is None:
            return False
        Subreddit = Query()
        x = self.UserBlacklist.contains(Subreddit.ID == subreddit.name)
        if bool(x):
            return True
        else:
            return False

    def add_subreddit(self, subreddit, Reason):
        if not self.CheckSubreddit(subreddit):
            self.log.info(f"Adding r/{subreddit} to the Blacklist for {Reason}")
            self.UserBlacklist.insert({"ID": subreddit, "Reason": Reason})
        else:
            self.log.info(
                f"Failed to add {subreddit} to the Blacklist Because r/{subreddit} is already on it"
            )

    def remove_subreddit(self, subreddit):
        Subreddits = Query()
        self.log.info(f"Removing {subreddit} to the Blacklist")
        self.UserBlacklist.remove(Subreddits.ID == subreddit)
