import logging
import praw
from praw import exceptions
from os import environ
from dotenv import load_dotenv

ACTIVE = True
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="Log.log",
    filemode="w+",
    level=logging.INFO
)
log = logging.getLogger(__name__)

log.info('starting setup')
load_dotenv('settings.env')
CLIENT_SECRET = environ.get('CLIENT_SECRET')
CLIENT_ID = environ.get('CLIENT_ID')
PASSWORD = environ.get('ACCOUNT_PASSWORD')
USERNAME = environ.get('ACCOUNT_USERNAME')
CREATOR_USERNAME = environ.get('CREATOR_USERNAME')

GITHUB_USERNAME = environ.get('GITHUB_ACCOUNT_USERNAME')
GITHUB_TOKEN = environ.get('GITHUB_TOKEN')

VERSION = 0.56
from prawcore.exceptions import OAuthException, ResponseException
from utils.funcs import truncate
# To truncate messages (optional really)
import time  # To sleep
import json  # Save/Load config
import logging  # For logging... of course
import sys  # For various things

# Configure the logger
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

# GLOBALS===========================#
unsubscribers = {}
default_config = {'unsubscribed_users': []}


# ==================================#
# Functions=========================#


def save():
    """
    Save the unsubscribers to file
    """
    # Open "unsubscribers.json" and dump the unsubscribers to it
    with open('unsubscribers.json', 'w') as f:
        json.dump(unsubscribers, f, indent=4, separators=(',', ': '))


def footer_message():
    """
    Returns the constructed footer message.\n
    `bot` The currently running bot.
    """
    # This can be customised to whatever you like. You can use Reddit Markdown formatting as well.
    return f'\n\n___\n\n ^(I am a bot. Message) u/{CREATOR_USERNAME} ^(if I am being stupid.) ^(If not Please consider) [^(Buying my creator a coffee.)](https://www.buymeacoffee.com/edoc) ^(We also have a) [^(Discord Server)](https://discord.gg/6EFAqm5aSG)^(,) ^(Come check it out.) ^[Unsubscribe](https://www.reddit.com/message/compose/?to={USERNAME}&subject=unsubscribe&message=unsubscribe)'


def login():
    log.info('initializing praw')
    # Try loading the config and logging in
    try:
        global unsubscribers
        with open('unsubscribers.json', 'r') as f:
            unsubscribers = json.load(f)

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
    # unsubscribers file doesn't exist
    except FileNotFoundError:
        log.warning(
            'Couldn\'t find "unsubscribers.json", creating...')
        with open('unsubscribers.json', 'w') as f:
            json.dump(default_config, f, indent=4, separators=(',', ': '))
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
        if message.author in unsubscribers['unsubscribed_users']:
            continue
        if bot.user.me() in [message.author for message in message.replies]:
            continue
        try:
            if message in bot.inbox.unread() and f'u/{USERNAME}' in message.body:  # if this message is a mention AND it is unread...
                log.info(
                    f'Found Mention in r/{str(message.subreddit)} (id:{str(message.id)})\n\t"' + truncate(message.body,
                                                                                                          70,
                                                                                                          '...') + '"')
                message.reply(f"hello, {message.author}"
                              f"{footer_message()}")  # reply with this message
                message.mark_read()  # mark message as read so your bot doesn't respond to it again...
        except praw.exceptions.APIException:  # Reddit may have rate limits, this prevents your bot from dying due to rate limits
            print("probably a rate limit....")


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
            unsubscribers['unsubscribed_users'].append(str(message.author))
            save()
            message.reply(
                f'Okay, I will no longer reply to your posts.{footer_message()}')
            message.delete()
        # Ignore the message if we don't recognise it
        else:
            message.delete()


def run_bot(bot: praw.Reddit, sleep_time: int = 3):
    handle_mentions(bot)
    handle_messages(bot)
    # Sleep, to not flood
    log.debug('Sleeping ' + str(sleep_time) + ' seconds...')
    time.sleep(sleep_time)


# ==================================#
def reply(message, content):
    message.reply(f'{content}{footer_message()}')


# Main Code=========================#
log.info('Logging in...')
global bot
bot = login()

log.info('Logged in as ' + str(bot.user.me()))
log.info(str(len(unsubscribers['unsubscribed_users'])) + ' unsubscribed user' + (
    's' if len(unsubscribers['unsubscribed_users']) != 1 else ''))

while True:
    run_bot(bot)
