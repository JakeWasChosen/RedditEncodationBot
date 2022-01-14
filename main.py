import sys  # For various things
# To truncate messages (optional really)
import time  # To sleep

import prawcore.exceptions
from praw import exceptions
from prawcore.exceptions import OAuthException, ResponseException

from utils.__init__ import BlackList as Blacklist
from utils.funcs import truncate
from utils.logic import *
from utils.vars import *

ACTIVE = True
logging.basicConfig(
    format='%(asctime)s - [%(name)s | %(filename)s:%(lineno)d] - %(levelname)s - %(message)s',
    filename="Log.log",
    filemode="w+",
    level=logging.DEBUG
)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('prawcore').setLevel(logging.WARNING)

log = logging.getLogger(__name__)

log.info('starting setup')
# Configure the logger
log.addHandler(logging.StreamHandler(sys.stdout))

# GLOBALS===========================#


# ==================================#
# Functions=========================#


def login():
    log.info('initializing praw')
    # Try loading the config and logging in
    try:
        # This block creates the Reddit api connection.
        r = praw.Reddit(username=USERNAME,
                        password=PASSWORD,
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        user_agent=f'u/{USERNAME}:v.{VERSION} (by /u/{CREATOR_USERNAME})')

        # Check credentials (if we can get "me", we're logged in!)
        r.user.me()
        log.info('praw initialized')
        return r
    # Couldn't log in to Reddit (probably wrong credentials)
    except (OAuthException, ResponseException) as e:
        log.error(
            'Invalid credentials.\nPlease check that the credentials in "settings.env" are correct.\n(' + str(e) + ')')
    input('Press return to exit...')
    exit(0)


def handle_mentions(bot: praw.Reddit):
    """
    Handle mentions
    `bot` The currently running bot\n
    """
    # For every subreddit bot should comment on

    messages = bot.inbox.stream()  # creates an iterable for your inbox and streams it
    for message in messages:  # iterates through your messages
        if message.author == bot.user.me():
            continue
        # Don't reply to unsubscribed users
        if Blacklist.CheckUser(message.author):
            message.mark_read()
        if Blacklist.CheckSubreddit(message.subreddit):
            message.mark_read()
        if bot.user.me() in [message.author for message in message.replies]:
            continue
        try:
            if message in bot.inbox.unread() and f'u/{USERNAME}' in message.body:  # if this message is a mention AND it is unread...
                log.info(
                    f'Found Mention in r/{str(message.subreddit)} (id:{str(message.id)})\n\t"' + truncate(message.body,
                                                                                                          70,
                                                                                                          '...') + '"')
                logic(bot, message)  # core logic of the bot
                message.mark_read()  # mark message as read so your bot doesn't respond to it again...
        except praw.exceptions.APIException:  # Reddit may have rate limits, this prevents your bot from dying due to rate limits
            log.debug("probably a rate limit....")


def handle_messages(bot: praw.Reddit, max_messages: int = 25):
    """
    Handle messages to the bot\n
    `bot` The currently running bot
    `max_messages` How many messages to search through
    """
    # Get the messages
    messages = list(bot.inbox.messages(limit=max_messages))
    # If we have no messages, quit
    if len(messages) == 0:
        return
    # Print how many messages we have
    log.info('Messages (' + str(len(messages)) + '):')
    # Iterate through every message
    for message in messages:
        log.info('Sender: ' + (str(message.author)
                               if message.author else 'Reddit'))
        log.info('\t"' + truncate(message.body, 70, '...') + '"')

        # This is where you can handle different text in the messages.
        # Unsubscribe user
        if 'unsubscribe' in message.subject.lower() or 'unsubscribe' in message.body.lower():
            log.info(f'Unsubscribing "{message.author}"')
            Blacklist.add_user(message.author, 'Unsubscribed')
            reply(message,
                  f'Okay, I will no longer reply to your posts.\n ^(If this was was a mistake please) ^[Resubscribe](https://www.reddit.com/message/compose/?to={USERNAME}&subject=resubscribe&message=resubscribe)')
            message.delete()
        # Ignore the message if we don't recognise it
        # Resubscribe user
        elif 'resubscribe' in message.subject.lower() or 'resubscribe' in message.body.lower():
            if Blacklist.CheckUserReason('Unsubscribed'):
                log.info(f'Resubscribing "{message.author}"')
                Blacklist.add_user(message.user, 'Unsubscribe')
                reply(message, f'Okay, I will no longer reply to your posts.')
                message.delete()
            else:
                log.info(f'{message.author} Tried to resubscribe but was blacklisted')
                reply(message,
                      f'Im Sorry, But you were Blacklisted\n^(If you believe this was a mistake please make an) [^(UnBlacklist Request)](https://github.com/JakeWasChosen/RedditEncodationBot/issues/new?assignees=JakeWasChosen&labels=UnblacklistRequest&template=unblacklist-request.md&title=)')
                message.deleted()
        else:
            log.info(f'Got a new message {message.subject}\n{message.body}')
            message.delete()


def run_bot(bot: praw.Reddit, sleep_time: int = 7):
    try:
        handle_messages(bot)
        handle_mentions(bot)
    except prawcore.exceptions.ServerError:
        sleep_time += 1
    # Sleep, to not flood
    log.debug('Sleeping ' + str(sleep_time) + ' seconds...')
    time.sleep(sleep_time)


# Main Code=========================#
log.info('Logging in...')
bot = login()
log.info('Logged in as ' + str(bot.user.me()))

while True:
    try:
        run_bot(bot)
    except prawcore.exceptions.RequestException:
        log.error('There was A prawcore.exceptions.RequestException')
        time.sleep(10)
