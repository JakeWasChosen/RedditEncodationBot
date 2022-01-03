import argparse
import logging
import shlex

import praw
from simplegist.simplegist import Simplegist

from main import GITHUB_TOKEN, GITHUB_USERNAME, footer_message, reply
from utils.vars import MorseCode, MorseCodeReversed

log = logging.getLogger(__name__)
ghg = Simplegist(username=GITHUB_USERNAME, api_token=GITHUB_TOKEN)

"""
Basic logic 
-e/encode : Encode
-d/decode : Decode

types:

-b64/base64 : Base64
"""


def logic(bot: praw.Reddit, message):
    typepicked = False
    argument = str(message.content).replace(f'u/{bot.user.me}', '')
    pr = argparse.ArgumentParser()
    pr.add_argument("--encode", "-e", help="Pick encode as your choice")
    pr.add_argument("--decode", "-d", help="Pick decode as your choice")
    pr.add_argument("--base32", "-b32", help="Encode/Decode in base32")
    pr.add_argument("--base64", "-b64", help="Encode/Decode in base64")
    pr.add_argument("--rot13", "-r13", help="Encode/Decode in rot13")
    pr.add_argument("--hex", "-h", help="Encode/Decode in hex")
    pr.add_argument("--base85", "-b85", help="Encode/Decode in base85")
    pr.add_argument("--ascii85", "-a85", help="Encode/Decode in ASCII85")
    pr.add_argument("--morse", "-m", help="Encode/Decode in morse code")
    pr.add_argument("--binary", "-b", help="Encode/Decode in binary")

    args = pr.parse_args(shlex.split(argument))

    # make sure the user picks encode or decode
    if not args.encode and not args.decode and not args.help:
        return warning(message, 'You need to pick either encode or decode')
    elif args.encode and args.encode:
        return warning(message, 'You can\'t pick both encode and decode')

    if args.base32:
        typepicked = True
    elif args.base64:
        typepicked = True
    else:
        warning(message, 'you need to fill in a least one of thease options')


import base64
import binascii
import codecs
from io import BytesIO


def encode(txt):
    """All encode methods"""
    pass


def decode(txt):
    """All decode methods"""
    pass


def warning(message, msg):
    log.warning(f'Message: {message} '
                f'{msg}')

    message.reply(f"{msg}"
                  f"{footer_message()}")


def InvalidWarning(message, param):
    log.info(f'Message: {message} '
             f'{param}')

    message.reply(f"Sorry {message.author} but it looks like that was some {param}, Please try again."
                  f"{footer_message()}")


def encryptout(message, ConversionType: str, text=None):
    """The main, modular function to control encrypt/decrypt commands"""
    if not text:
        return warning(message,
                       f"Aren't you going to give me anything to encode/decode **{message.author.name}**"
                       )
    # todo return if over 1500 chars in lengh a github gist
    if len(text) > 1500:
        try:
            data = BytesIO(text.encode("utf-8"))
        except AttributeError:
            data = BytesIO(text)
        try:
            content = f'**{ConversionType}**\n{data}'
            reply(message, content)

        except Exception as e:
            log.error(f'Somthing went wrong with {e}')
            return warning(message, f"Somthing went wrong, sorry {message.author}...")

    else:
        ghg.create(name='_GISTNAME', description='_ANY_DESCRIPTION', public=1, content='_CONTENT_GOES_HERE')


def CreateGist(message, content: str) -> str:
    return ghg.create(name=f'Encodation Post', description=f'Encodation feed for u/{message.author}', public=0,
                      content=content)

    # todo reply(f"📑 **{ConversionType}**```fix\n{text}```")


# @encode.command(name="base32", aliases=["b32"], brief="Encode in base32")
def encode_base32(message, text: str):
    encryptout(
        message, "Text -> base32", base64.b32encode(text.encode("utf-8"))
    )


# @decode.command(name="base32", aliases=["b32"], brief="Decode in base32")
def decode_base32(message, text: str):
    try:
        encryptout(
            message, "base32 -> Text", base64.b32decode(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid base32...")


# @encode.command(name="base64", aliases=["b64"], brief="Encode in base64")
def encode_base64(message, text: str):
    encryptout(
        message, "Text -> base64", base64.urlsafe_b64encode(text.encode("utf-8"))
    )


# @decode.command(name="base64", aliases=["b64"], brief="Decode in base64")
def decode_base64(message, text: str):
    try:
        encryptout(
            message, "base64 -> Text", base64.urlsafe_b64decode(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid base64...")


# @encode.command(name="rot13", aliases=["r13"], brief="Encode in rot13")
def encode_rot13(message, text: str):
    encryptout(message, "Text -> rot13", codecs.decode(text, "rot_13"))


# @decode.command(name="rot13", aliases=["r13"], brief="Decode in rot13")
def decode_rot13(message, text: str):
    try:
        encryptout(message, "rot13 -> Text", codecs.decode(text, "rot_13"))
    except Exception:
        InvalidWarning(message, "Invalid rot13...")


# @encode.command(name="hex", brief="Encode in hex")
def encode_hex(message, text: str):
    encryptout(
        message, "Text -> hex", binascii.hexlify(text.encode("utf-8"))
    )


# @decode.command(name="hex", brief="Decode in hex")
def decode_hex(message, text: str):
    try:
        encryptout(
            message, "hex -> Text", binascii.unhexlify(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid hex...")


# @encode.command(name="base85", aliases=["b85"], brief="Encode in base85")
def encode_base85(message, text: str):
    encryptout(
        message, "Text -> base85", base64.b85encode(text.encode("utf-8"))
    )


# @decode.command(name="base85", aliases=["b85"], brief="Decode in base85")
def decode_base85(message, text: str):
    try:
        encryptout(
            message, "base85 -> Text", base64.b85decode(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid base85...")


# @encode.command(name="ascii85", aliases=["a85"], breif="Encode in ASCII85")
def encode_ascii85(message, text: str):
    encryptout(
        message, "Text -> ASCII85", base64.a85encode(text.encode("utf-8"))
    )


# @decode.command(name="ascii85", aliases=["a85"], brief="Decode in ASCII85")
def decode_ascii85(message, text: str):
    try:
        encryptout(
            message, "ASCII85 -> Text", base64.a85decode(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid ASCII85...")


# @encode.command(name="morse", brief="Encode in morse code")
def encode_to_morse(message, text: str):
    try:
        answer = " ".join(MorseCode.get(i.upper()) for i in text)
    except TypeError:
        return InvalidWarning(message, 'Invalid Morse')
    encryptout(message, "Text -> Morse", answer)


# @decode.command(name="morse", brief="Decode to morse code")
def decode_to_morse(message, text: str):
    try:
        answer = " ".join(MorseCodeReversed.get(i.upper()) for i in text.split())
    except TypeError:
        return InvalidWarning(message, 'Invalid Morse')
    encryptout(message, "Morse -> Text", answer)


# @encode.command(name="binary", aliases=["b"], brief="Encode to binary")
def encode_to_binary(message, text: str):
    try:
        res = ''.join(format(ord(i), '08b') for i in text)
    except TypeError:
        return InvalidWarning(message, 'Invalid Binary')
    encryptout(
        message, "Text -> binary", res)


# @decode.command(name="binary", aliases=["b"], brief="Decode in binary")
def decode_from_binary(message, text: str):
    try:
        binary_int = int(text, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode()
    except TypeError:
        return InvalidWarning(message, 'Invalid Binary')
    encryptout(
        message, "Binary -> Text", ascii_text)
