import argparse
import base64
import binascii
import codecs
import logging
import shlex

import praw

from utils.database import request
from utils.funcs import (
    create_gist,
    reply,
    remove_markdown,
    unlistify,
    log_codec,
    log_codec_completion,
    send_help,
)
from utils.vars import MorseCode, MorseCodeReversed, footer_message

log = logging.getLogger(__name__)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        log.info(f"error: {message}")


def logic(bot: praw.Reddit, message):
    argument = remove_markdown(str(message.body).replace(f"u/{str(bot.user.me())}", ""))
    pr = MyParser(exit_on_error=False, add_help=False)
    pr.add_argument(
        "--encode", "-e", "-enc", help="Pick encode as your choice", action="store_true"
    )
    pr.add_argument(
        "--decode", "-d", "-dec", help="Pick decode as your choice", action="store_true"
    )
    pr.add_argument(
        "--base32", "-b32", help="Encode/Decode in base32", action="store_true"
    )
    pr.add_argument(
        "--base64", "-b64", help="Encode/Decode in base64", action="store_true"
    )
    pr.add_argument(
        "--rot13", "-r13", help="Encode/Decode in rot13", action="store_true"
    )
    pr.add_argument(
        "--hex", "-he", "-hex", help="Encode/Decode in hex", action="store_true"
    )
    pr.add_argument(
        "--base85", "-b85", help="Encode/Decode in base85", action="store_true"
    )
    pr.add_argument(
        "--ascii85", "-a85", help="Encode/Decode in ASCII85", action="store_true"
    )
    pr.add_argument(
        "--morse", "-m", help="Encode/Decode in morse code", action="store_true"
    )
    pr.add_argument(
        "--binary", "-b", "-bin", help="Encode/Decode in binary", action="store_true"
    )
    pr.add_argument("--text", "-t", help="the text (optional)")
    pr.add_argument("-h", "--help", help="show this help message", action="store_true")
    try:

        args, text = pr.parse_known_args(shlex.split(argument))
    except Exception:
        return warning(
            message,
            "Your message couldn't parse, Please make sure y ou are using the correct args",
        )
    request(message, args)
    if not bool(argument) or str(argument).replace(" ", "").lower() == "help":
        return send_help(message, pr)
    log.debug(f"{args=} | {argument=}")
    text = unlistify(text) or args.text
    str(text).replace("&#x200b", "").replace("\n\n", "")
    if not text and not args.help:  # FIXME this might be useless
        return warning(message, "you need to fill the --text argument")
    # types
    if args.help:
        send_help(message, pr)
    if args.base32:
        log_codec(message, "b32")
        codec = "base32"
    elif args.base64:
        log_codec(message, "64")
        codec = "base64"
    elif args.base85:
        log_codec(message, "85")
        codec = "base85"
    elif args.rot13:
        log_codec(message, "rot13")
        codec = "rot13"
    elif args.hex:
        log_codec(message, "hex")
        codec = "hex"
    elif args.ascii85:
        log_codec(message, "ascii85")
        codec = "ascii85"
    elif args.morse:
        log_codec(message, "morse")
        codec = "morse"
    elif args.binary:

        log_codec(message, "binary")
        codec = "binary"
    else:
        return warning(
            message,
            "you need to fill in a least one of codec options ^(do -h for help)",
        )

    if args.encode:
        encode(codec, message, text)
    elif args.decode:
        decode(codec, message, text)

    if not args.encode and not args.decode:
        return warning(
            message, "You need to pick either encode or decode\ne.g. -e -b32 hey"
        )
    elif args.encode and args.decode:
        return warning(message, "You can't pick both encode and decode")


def encode(codec, message, txt):
    """All encode methods"""
    match codec:
        case "base32":
            encode_base32(message, txt)
        case "base64":
            encode_base64(message, txt)
        case "base85":
            encode_base85(message, txt)
        case "rot13":
            encode_rot13(message, txt)
        case "hex":
            encode_hex(message, txt)
        case "ascii85":
            encode_ascii85(message, txt)
        case "morse":
            encode_morse(message, txt)
        case "binary":
            encode_binary(message, txt)


def decode(codec, message, txt):
    """All decode methods"""
    match codec:
        case "base32":
            decode_base32(message, txt)
        case "base64":
            decode_base64(message, txt)
        case "base85":
            decode_base85(message, txt)
        case "rot13":
            decode_rot13(message, txt)
        case "hex":
            decode_hex(message, txt)
        case "ascii85":
            decode_ascii85(message, txt)
        case "morse":
            decode_morse(message, txt)
        case "binary":
            decode_binary(message, txt)


def warning(message, msg):
    log.warning(f"Message: {message} " f"{msg}")
    reply(message, msg)


def InvalidWarning(message, param):
    log.info(f"Message: {message} " f"{param}")

    message.reply(
        f"Sorry u/{message.author} but it looks like that was some {param}, Please try again."
        f"{footer_message()}"
    )


def encryptout(message, ConversionType: str, text):
    print(text)
    """The main, modular function to control encrypt/decrypt commands"""
    if not text:
        return warning(
            message,
            f"Aren't you going to give me anything to encode/decode **{message.author.name}**",
        )
    try:
        text = str(text, "utf-8").replace("\n", "")
    except Exception:
        pass
    to, from_ = tuple(ConversionType.split(" -> "))
    log_codec_completion(message, to, from_)
    try:
        content = f"*{ConversionType}*\n`{text}`"
    except Exception as e:
        log.error(f"Something went wrong with {e}")
        return warning(message, f"Something went wrong, sorry u/{message.author}...")

    if len(text) < 1500:
        reply(message, content)

    else:
        log.debug(f"Creating Gist {message.id}")
        CreateGistMessage(message, content=content)


def CreateGistMessage(message, content: str):
    return reply(
        message,
        content=f"The text was a bit long so I put it in a gist {CreateGist(message, content)}",
    )


def CreateGist(message, content: str) -> str:
    return create_gist(
        description=f"Encodation feed for u/{message.author}", content=content
    )


def encode_base32(message, text: str):
    encryptout(message, "Text -> base32", base64.b32encode(text.encode("utf-8")))


def decode_base32(message, text: str):
    try:
        encryptout(message, "base32 -> Text", base64.b32decode(text.encode("utf-8")))
    except Exception:
        InvalidWarning(message, "Invalid base32...")


def encode_base64(message, text: str):
    encryptout(
        message, "Text -> base64", base64.urlsafe_b64encode(text.encode("utf-8"))
    )


def decode_base64(message, text: str):
    try:
        encryptout(
            message, "base64 -> Text", base64.urlsafe_b64decode(text.encode("utf-8"))
        )
    except Exception:
        InvalidWarning(message, "Invalid base64...")


def encode_rot13(message, text: str):
    encryptout(message, "Text -> rot13", codecs.decode(text, "rot_13"))


def decode_rot13(message, text: str):
    try:
        encryptout(message, "rot13 -> Text", codecs.decode(text, "rot_13"))
    except Exception:
        InvalidWarning(message, "Invalid rot13...")


def encode_hex(message, text: str):
    try:
        encryptout(message, "Text -> hex", binascii.hexlify(text.encode()))
    except Exception:
        InvalidWarning(message, "Invalid hex...")


def decode_hex(message, text: str):
    try:
        encryptout(message, "hex -> Text", bytearray.fromhex(text).decode("utf-8"))
    except Exception:
        InvalidWarning(message, "Invalid hex...")


def encode_base85(message, text: str):
    encryptout(message, "Text -> base85", base64.b85encode(text.encode("utf-8")))


def decode_base85(message, text: str):
    try:
        encryptout(message, "base85 -> Text", base64.b85decode(text.encode("utf-8")))
    except Exception:
        InvalidWarning(message, "Invalid base85...")


def encode_ascii85(message, text: str):
    encryptout(message, "Text -> ASCII85", base64.a85encode(text.encode("utf-8")))


def decode_ascii85(message, text: str):
    try:
        encryptout(message, "ASCII85 -> Text", base64.a85decode(text.encode("utf-8")))
    except Exception:
        InvalidWarning(message, "Invalid ASCII85...")


def encode_morse(message, text: str):
    try:
        answer = "".join(MorseCode.get(i.upper()) for i in text)
    except TypeError:
        return InvalidWarning(message, "Invalid Morse")
    encryptout(message, "Text -> Morse", answer)


def decode_morse(message, text: str):
    try:
        answer = "".join(MorseCodeReversed.get(i.upper()) for i in text.split())
    except TypeError:
        return InvalidWarning(message, "Invalid Morse")
    encryptout(message, "Morse -> Text", answer)


def encode_binary(message, text: str):
    try:
        res = "".join(format(ord(i), "08b") for i in text)
    except TypeError:
        return InvalidWarning(message, "Invalid Binary")
    encryptout(message, "Text -> binary", res)


def decode_binary(message, text: str):
    try:
        binary_int = int(text, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode()
    except TypeError:
        return InvalidWarning(message, "Invalid Binary")
    encryptout(message, "Binary -> Text", ascii_text)
