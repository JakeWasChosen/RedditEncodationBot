import logging
from functools import lru_cache
from os import environ
from dotenv import load_dotenv

log = logging.getLogger(__name__)
log.info('loading env vars')
load_dotenv('settings.env')
CLIENT_SECRET = environ.get('CLIENT_SECRET')
CLIENT_ID = environ.get('CLIENT_ID')
PASSWORD = environ.get('ACCOUNT_PASSWORD')
USERNAME = environ.get('ACCOUNT_USERNAME')
CREATOR_USERNAME = environ.get('CREATOR_USERNAME')

GITHUB_TOKEN = environ.get('GITHUB_TOKEN')

VERSION = 0.56

@lru_cache(maxsize=50)
def footer_message():
    """
    Returns the constructed footer message.\n
    `bot` The currently running bot.
    """
    # This can be customised to whatever you like. You can use Reddit Markdown formatting as well.
    return f'\n\n___\n\n ^(I am a bot. Please message) [^(u/{CREATOR_USERNAME})](https://www.reddit.com/u/{CREATOR_USERNAME}/) ^(if I am being stupid.) ^(If not Please consider) [^(Buying my creator a coffee.)](https://www.buymeacoffee.com/edoc) ^(We also have a) [^(Discord Server)](https://discord.gg/6EFAqm5aSG)^(,) ^(Come check it out.)\n ^[Unsubscribe](https://www.reddit.com/message/compose/?to={USERNAME}&subject=unsubscribe&message=unsubscribe)'


_MARKDOWN_ESCAPE_COMMON = r'^>(?:>>)?\s|\[.+\]\(.+\)'

_URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'

_MARKDOWN_STOCK_REGEX = fr'(?P<markdown>[_\\~|\*`]|{_MARKDOWN_ESCAPE_COMMON})'
MorseCode = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    " ": "/",
}
MorseCodeReversed = {
    "..-.": "f",
    "-..-": "x",
    "/": " ",
    ".--.": "p",
    "-": "t",
    "..---": "2",
    "....-": "4",
    "-----": "0",
    "--...": "7",
    "...-": "v",
    "-.-.": "c",
    ".": "e",
    ".---": "j",
    "---": "o",
    "-.-": "k",
    "----.": "9",
    "..": "i ",
    ".-..": "l",
    ".....": "5",
    "...--": "3",
    "-.--": "y",
    "-....": "6",
    ".--": "w",
    "....": "h",
    "-.": "n",
    ".-.": "r",
    "-...": "b",
    "---..": "8",
    "--..": "z",
    "-..": "d",
    "--.-": "q",
    "--.": "g",
    "--": "m",
    "..-": "u",
    ".-": "a",
    "...": "s",
    ".----": "1",
}
